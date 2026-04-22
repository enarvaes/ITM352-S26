# Quiz Game - Web Application
# Name: Ethan Narvaes
# Date: April 21, 2026
# Based on: Assignment 1 (Console Quiz Game)
# Converts the console quiz from Assignment 1 into a Flask web app.
# Individual requirements implemented:
#   1. Persistent User Identification and History (sessions + users.json)
#   2. Leaderboard System (scores.json + /leaderboard)
# Extra credit: Answer Explanations and Responsive Design.

import json
import os
import random
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

from flask import Flask, render_template, request, jsonify, session, redirect, url_for

# Keep data file paths near the top so they are easy to change.
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
QUESTIONS_FILE = DATA_DIR / "questions.json"
SCORES_FILE = DATA_DIR / "scores.json"
USERS_FILE = DATA_DIR / "users.json"

# Which extra credit features are turned on. Keeping this as a dict makes it
# easy to flip features without hunting through templates.
EXTRAS_ENABLED = {
    "timer": False,
    "progress_bar": False,
    "explanations": True,
    "responsive": True,
}

app = Flask(__name__)
app.secret_key = "quiz_game_secret_key_itm352"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

# Quiz state for currently-active quizzes. Keyed by user_id so two people
# taking quizzes at the same time don't collide. This is in-memory only,
# which is fine because it's just the current question order; finished
# scores still get saved to scores.json.
active_quizzes = {}


@app.context_processor
def inject_extras():
    # Make the extras flags available to every template as `extras_enabled`.
    return dict(extras_enabled=EXTRAS_ENABLED)


def load_json_file(filepath):
    # Return {} for dict-shaped files and [] for list-shaped files if the
    # file is missing or corrupt. Keeps the rest of the code simple.
    try:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    name = str(filepath).lower()
    if "questions" in name:
        return []
    return {}


def save_json_file(filepath, data):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as error:
        print(f"Error saving file {filepath}: {error}")


def start_new_quiz(user_id):
    """Pick a random question order for this user and cache it in memory."""
    # Previously I called load_questions() inside every API route, but each
    # call re-shuffled the list so the "correct answer" for question 0
    # was coming from a different shuffle than the question the user
    # actually saw. Caching the shuffled list per user fixes that.
    questions = load_json_file(QUESTIONS_FILE)
    random.shuffle(questions)
    for q in questions:
        if "options" in q:
            options = list(q["options"])
            random.shuffle(options)
            q["options"] = options

    quiz_id = str(random.randint(100000, 999999))
    active_quizzes[user_id] = {
        "quiz_id": quiz_id,
        "questions": questions,
        "answers": [None] * len(questions),
        "started_at": datetime.now(),
    }
    return active_quizzes[user_id]


def get_active_quiz(user_id):
    return active_quizzes.get(user_id)


def login_required(f):
    # AI-assisted (Claude): this is the standard Flask login-required
    # decorator pattern. I kept it because I understood what it does
    # (redirect to /login if session['user_id'] isn't set).
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


# ---- Page routes ----

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Allow form posts from the login page or JSON posts from fetch().
        data = request.get_json() if request.is_json else request.form
        name = data.get("name", "").strip()

        if not name or len(name) < 2:
            error = "Name must be at least 2 characters"
            if request.is_json:
                return jsonify({"success": False, "error": error})
            return render_template("login.html", error=error)

        users = load_json_file(USERS_FILE)

        # Case-insensitive lookup so "Ethan" and "ethan" are the same user.
        user_id = None
        for uid, user_data in users.items():
            if user_data["name"].lower() == name.lower():
                user_id = uid
                break

        now = datetime.now().isoformat()
        if not user_id:
            # Make a new user id that is one higher than the current max.
            existing_ids = [int(uid) for uid in users.keys() if uid.isdigit()]
            user_id = str(max(existing_ids, default=0) + 1)
            users[user_id] = {
                "name": name,
                "created_at": now,
                "last_login": now,
            }
        else:
            users[user_id]["last_login"] = now
        save_json_file(USERS_FILE, users)

        session["user_id"] = user_id
        session["user_name"] = users[user_id]["name"]
        session.permanent = True

        if request.is_json:
            return jsonify({"success": True, "redirect": url_for("dashboard")})
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # Drop any cached quiz for this user so it doesn't leak memory.
    user_id = session.get("user_id")
    if user_id and user_id in active_quizzes:
        del active_quizzes[user_id]
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    user_name = session["user_name"]

    scores = load_json_file(SCORES_FILE)
    user_scores = scores.get(user_id, [])

    total_quizzes = len(user_scores)
    if user_scores:
        avg_score = sum(s["score"] for s in user_scores) / total_quizzes
        best_score = max(s["score"] for s in user_scores)
    else:
        avg_score = 0
        best_score = 0

    return render_template(
        "dashboard.html",
        user_name=user_name,
        total_quizzes=total_quizzes,
        avg_score=round(avg_score, 2),
        best_score=best_score,
        recent_scores=user_scores[-5:],
    )


@app.route("/quiz")
@login_required
def quiz():
    return render_template("quiz.html")


@app.route("/results")
@login_required
def results():
    # Cast to numbers so the template can do math like correct/total.
    try:
        score = float(request.args.get("score", 0))
        correct = int(request.args.get("correct", 0))
        total = int(request.args.get("total", 0))
        time_taken = int(request.args.get("time_taken", 0))
    except ValueError:
        score, correct, total, time_taken = 0, 0, 0, 0

    if total <= 0:
        # Avoid a divide-by-zero in the results template.
        total = 1
    return render_template(
        "results.html",
        score=score,
        correct=correct,
        total=total,
        time_taken=time_taken,
    )


@app.route("/leaderboard")
def leaderboard():
    scores = load_json_file(SCORES_FILE)
    users = load_json_file(USERS_FILE)

    rankings = []
    for user_id, user_scores in scores.items():
        if user_scores and user_id in users:
            avg_score = sum(s["score"] for s in user_scores) / len(user_scores)
            best_score = max(s["score"] for s in user_scores)
            rankings.append({
                "user_id": user_id,
                "name": users[user_id]["name"],
                "avg_score": round(avg_score, 2),
                "best_score": round(best_score, 2),
                "quizzes_taken": len(user_scores),
            })

    # Rank by best score first, then average as a tiebreaker.
    rankings.sort(key=lambda x: (x["best_score"], x["avg_score"]), reverse=True)
    top_10 = rankings[:10]

    current_user_id = session.get("user_id")
    current_user_rank = None
    if current_user_id:
        for i, entry in enumerate(rankings, start=1):
            if entry["user_id"] == current_user_id:
                current_user_rank = i
                break

    return render_template(
        "leaderboard.html",
        leaderboard=top_10,
        current_user_rank=current_user_rank,
        current_user_id=current_user_id,
    )


# ---- REST API ----

@app.route("/api/quiz-start", methods=["POST"])
@login_required
def api_quiz_start():
    user_id = session["user_id"]
    data = request.get_json() or {}
    mode = data.get("mode", "normal")
    time_limit = data.get("time_limit", 300)

    quiz_state = start_new_quiz(user_id)
    if not quiz_state["questions"]:
        return jsonify({"success": False, "error": "No questions available"})

    # Remember mode and time limit for when we save the result.
    session["quiz_mode"] = mode
    session["quiz_time_limit"] = time_limit
    session["quiz_id"] = quiz_state["quiz_id"]

    first = quiz_state["questions"][0]
    return jsonify({
        "success": True,
        "quiz_id": quiz_state["quiz_id"],
        "total_questions": len(quiz_state["questions"]),
        "mode": mode,
        "time_limit": time_limit,
        "question": {
            "id": 0,
            "text": first["question"],
            "options": first["options"],
        },
    })


@app.route("/api/question/<int:question_id>", methods=["GET"])
@login_required
def api_get_question(question_id):
    user_id = session["user_id"]
    quiz_state = get_active_quiz(user_id)
    if not quiz_state:
        return jsonify({"success": False, "error": "No active quiz. Start a new quiz first."})

    questions = quiz_state["questions"]
    if question_id < 0 or question_id >= len(questions):
        return jsonify({"success": False, "error": "Question not found"})

    q = questions[question_id]
    return jsonify({
        "success": True,
        "question": {
            "id": question_id,
            "text": q["question"],
            "options": q["options"],
            "total": len(questions),
        },
    })


@app.route("/api/submit-answer", methods=["POST"])
@login_required
def api_submit_answer():
    user_id = session["user_id"]
    quiz_state = get_active_quiz(user_id)
    if not quiz_state:
        return jsonify({"success": False, "error": "No active quiz"})

    data = request.get_json() or {}
    question_id = data.get("question_id")
    selected_answer = data.get("answer")

    questions = quiz_state["questions"]
    if not isinstance(question_id, int) or question_id < 0 or question_id >= len(questions):
        return jsonify({"success": False, "error": "Invalid question"})

    q = questions[question_id]
    correct_answer = q["correct_answer"]
    is_correct = (selected_answer == correct_answer)

    # Record this answer so the server computes the final score, not the
    # client. A previous version trusted the client-side "correctCount"
    # which could double-count if the user went back and re-answered.
    quiz_state["answers"][question_id] = {
        "selected": selected_answer,
        "is_correct": is_correct,
    }

    return jsonify({
        "success": True,
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "explanation": q.get("explanation", ""),
        "next_question_id": question_id + 1,
    })


@app.route("/api/submit-quiz", methods=["POST"])
@login_required
def api_submit_quiz():
    user_id = session["user_id"]
    quiz_state = get_active_quiz(user_id)
    if not quiz_state:
        return jsonify({"success": False, "error": "No active quiz"})

    data = request.get_json() or {}
    time_taken = data.get("time_taken", 0)

    # Count correct answers from the server-side record, not from the client.
    answers = quiz_state["answers"]
    total_count = len(answers)
    correct_count = sum(1 for a in answers if a and a.get("is_correct"))
    score = round((correct_count / total_count * 100), 2) if total_count > 0 else 0

    scores = load_json_file(SCORES_FILE)
    if user_id not in scores:
        scores[user_id] = []
    scores[user_id].append({
        "quiz_id": quiz_state["quiz_id"],
        "date": datetime.now().isoformat(),
        "score": score,
        "correct": correct_count,
        "total": total_count,
        "time_taken": time_taken,
        "mode": session.get("quiz_mode", "normal"),
    })
    save_json_file(SCORES_FILE, scores)

    # Quiz is done so clear the cached state.
    del active_quizzes[user_id]

    return jsonify({
        "success": True,
        "score": score,
        "correct": correct_count,
        "total": total_count,
        "time_taken": time_taken,
    })


# ---- Error handlers ----

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


def ensure_data_files():
    # Create the data folder and empty JSON files on first run so the app
    # doesn't crash when the user hasn't created them yet.
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(QUESTIONS_FILE):
        save_json_file(QUESTIONS_FILE, [])
    if not os.path.exists(SCORES_FILE):
        save_json_file(SCORES_FILE, {})
    if not os.path.exists(USERS_FILE):
        save_json_file(USERS_FILE, {})


if __name__ == "__main__":
    ensure_data_files()
    app.run(debug=True, host="127.0.0.1", port=5000)
