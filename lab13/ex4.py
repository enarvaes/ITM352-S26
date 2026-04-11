import json
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "lab13-ex4-quiz-skeleton"


def load_a1_questions():
	question_file = Path(__file__).resolve().parent.parent / "Assignment 1" / "question.json"
	with question_file.open(encoding="utf-8") as file:
		data = json.load(file)

	if not data:
		return "General", []

	category = next(iter(data.keys()))
	questions = data.get(category, [])
	return category, questions


CATEGORY, QUESTIONS = load_a1_questions()


@app.route("/")
def home():
	return render_template("quiz_index.html")


@app.route("/quiz")
def quiz_landing():
	session["answers"] = {}
	return render_template(
		"quiz_take.html",
		total_questions=len(QUESTIONS),
		category=CATEGORY,
	)


@app.route("/quiz/question/<int:question_id>", methods=["GET", "POST"])
def quiz_question(question_id):
	if question_id < 1 or question_id > len(QUESTIONS):
		return render_template("quiz_not_found.html", question_id=question_id), 404

	if request.method == "POST":
		selected_answer = request.form.get("answer")
		if selected_answer is not None:
			answers = session.get("answers", {})
			answers[str(question_id)] = int(selected_answer)
			session["answers"] = answers

		if question_id >= len(QUESTIONS):
			return redirect(url_for("quiz_results"))
		return redirect(url_for("quiz_question", question_id=question_id + 1))

	question = QUESTIONS[question_id - 1]
	selected_answer = session.get("answers", {}).get(str(question_id))
	is_last = question_id == len(QUESTIONS)

	return render_template(
		"quiz_question.html",
		question=question,
		question_id=question_id,
		total_questions=len(QUESTIONS),
		selected_answer=selected_answer,
		is_last=is_last,
	)


@app.route("/quiz/results")
def quiz_results():
	answers = session.get("answers", {})
	correct = 0
	results = []

	for index, question in enumerate(QUESTIONS, start=1):
		selected_index = answers.get(str(index))
		is_correct = selected_index in question.get("correct_indices", [])
		if is_correct:
			correct += 1

		selected_text = "No answer"
		if isinstance(selected_index, int) and 0 <= selected_index < len(question["options"]):
			selected_text = question["options"][selected_index]

		correct_text = ", ".join(
			question["options"][i]
			for i in question.get("correct_indices", [])
			if 0 <= i < len(question["options"])
		)

		results.append(
			{
				"question": question["question"],
				"selected": selected_text,
				"correct": correct_text,
				"is_correct": is_correct,
				"explanation": question.get("explanation", ""),
			}
		)

	total = len(QUESTIONS)
	incorrect = total - correct
	percent = round((correct / total) * 100, 1) if total else 0

	return render_template(
		"quiz_results.html",
		category=CATEGORY,
		total=total,
		correct=correct,
		incorrect=incorrect,
		percent=percent,
		results=results,
	)


@app.route("/about")
def about():
	return render_template("quiz_about.html")


if __name__ == "__main__":
	app.run(debug=True)
