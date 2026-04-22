# Tests for Quiz Game Web Application
# Name: Ethan Narvaes
# Date: April 21, 2026
# Run with: python test_app.py  (or: python -m unittest test_app)
#
# These tests spin up the Flask test client and hit the routes. Each test
# class points the app at a temporary data directory so the real
# data/users.json and data/scores.json files are not touched.

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import app as app_module
from app import app, load_json_file, save_json_file


class QuizAppTestCase(unittest.TestCase):

    def setUp(self):
        # Redirect the app's data files to a temporary folder so tests do
        # not write to the real users.json / scores.json.
        self.test_dir = tempfile.mkdtemp()
        self._orig_data_dir = app_module.DATA_DIR
        self._orig_questions = app_module.QUESTIONS_FILE
        self._orig_scores = app_module.SCORES_FILE
        self._orig_users = app_module.USERS_FILE

        app_module.DATA_DIR = Path(self.test_dir)
        app_module.QUESTIONS_FILE = Path(self.test_dir) / "questions.json"
        app_module.SCORES_FILE = Path(self.test_dir) / "scores.json"
        app_module.USERS_FILE = Path(self.test_dir) / "users.json"

        # Copy the real questions.json into the temp dir so the quiz has
        # something to load during tests.
        real_questions = Path(__file__).parent / "data" / "questions.json"
        if real_questions.exists():
            shutil.copy(real_questions, app_module.QUESTIONS_FILE)
        else:
            save_json_file(app_module.QUESTIONS_FILE, [])
        save_json_file(app_module.USERS_FILE, {})
        save_json_file(app_module.SCORES_FILE, {})

        # Clear any quiz state left over from a previous test.
        app_module.active_quizzes.clear()

        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        # Put the original file paths back so other test runs are not affected.
        app_module.DATA_DIR = self._orig_data_dir
        app_module.QUESTIONS_FILE = self._orig_questions
        app_module.SCORES_FILE = self._orig_scores
        app_module.USERS_FILE = self._orig_users
        shutil.rmtree(self.test_dir, ignore_errors=True)
        app_module.active_quizzes.clear()

    def login_as(self, name):
        # Helper: log in with form data like the login page does.
        return self.client.post("/login", data={"name": name}, follow_redirects=False)

    # ---- Authentication ----

    def test_home_redirects_to_login_when_logged_out(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_login_page_loads(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Quiz Game", response.data)

    def test_login_with_valid_name_creates_user(self):
        self.login_as("Ethan")
        users = load_json_file(app_module.USERS_FILE)
        names = [u["name"] for u in users.values()]
        self.assertIn("Ethan", names)

    def test_login_short_name_rejected(self):
        response = self.client.post("/login", data={"name": "A"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"at least 2 characters", response.data)

    def test_returning_user_recognized_by_case_insensitive_name(self):
        self.login_as("Ethan")
        self.client.get("/logout")
        # Log in with a different case - should reuse the same user id.
        self.login_as("ETHAN")
        users = load_json_file(app_module.USERS_FILE)
        self.assertEqual(len(users), 1)

    def test_logout_clears_session(self):
        self.login_as("Ethan")
        response = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # ---- Protected pages ----

    def test_dashboard_requires_login(self):
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads_after_login(self):
        self.login_as("Ethan")
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Ethan", response.data)

    def test_quiz_page_requires_login(self):
        response = self.client.get("/quiz")
        self.assertEqual(response.status_code, 302)

    # ---- Quiz API ----

    def test_quiz_start_requires_login(self):
        response = self.client.post("/api/quiz-start", json={"mode": "normal"})
        self.assertEqual(response.status_code, 302)

    def test_quiz_start_returns_first_question(self):
        self.login_as("Ethan")
        response = self.client.post("/api/quiz-start", json={"mode": "normal"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertGreater(data["total_questions"], 0)
        self.assertIn("text", data["question"])
        self.assertIn("options", data["question"])

    def test_questions_stay_consistent_across_api_calls(self):
        # This is the key regression test. Before the fix, every API call
        # re-shuffled the question list, so question 0 from quiz-start was
        # a different question than /api/question/0 returned.
        self.login_as("Ethan")
        start = self.client.post("/api/quiz-start", json={"mode": "normal"}).get_json()
        first_from_start = start["question"]["text"]
        first_from_get = self.client.get("/api/question/0").get_json()["question"]["text"]
        self.assertEqual(first_from_start, first_from_get)

    def test_get_question_out_of_range(self):
        self.login_as("Ethan")
        self.client.post("/api/quiz-start", json={"mode": "normal"})
        response = self.client.get("/api/question/999")
        data = response.get_json()
        self.assertFalse(data["success"])

    def test_submit_answer_marks_correct(self):
        # Start a quiz, look at question 0's correct_answer from the
        # server's cache, submit that same answer, and check is_correct.
        self.login_as("Ethan")
        self.client.post("/api/quiz-start", json={"mode": "normal"})
        user_id = None
        with self.client.session_transaction() as sess:
            user_id = sess.get("user_id")
        correct_answer = app_module.active_quizzes[user_id]["questions"][0]["correct_answer"]

        response = self.client.post("/api/submit-answer",
                                    json={"question_id": 0, "answer": correct_answer})
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertTrue(data["is_correct"])

    def test_submit_answer_marks_wrong(self):
        self.login_as("Ethan")
        self.client.post("/api/quiz-start", json={"mode": "normal"})
        response = self.client.post("/api/submit-answer",
                                    json={"question_id": 0, "answer": "DEFINITELY_NOT_A_REAL_OPTION"})
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertFalse(data["is_correct"])

    def test_submit_quiz_computes_score_from_server_side_answers(self):
        # Answer every question correctly and check the final score is 100.
        self.login_as("Ethan")
        self.client.post("/api/quiz-start", json={"mode": "normal"})
        user_id = None
        with self.client.session_transaction() as sess:
            user_id = sess.get("user_id")
        questions = app_module.active_quizzes[user_id]["questions"]

        for i, q in enumerate(questions):
            self.client.post("/api/submit-answer",
                             json={"question_id": i, "answer": q["correct_answer"]})

        response = self.client.post("/api/submit-quiz", json={"time_taken": 120})
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["score"], 100.0)
        self.assertEqual(data["correct"], len(questions))

    def test_submit_quiz_saves_to_scores_file(self):
        self.login_as("Ethan")
        self.client.post("/api/quiz-start", json={"mode": "normal"})
        self.client.post("/api/submit-quiz", json={"time_taken": 100})
        scores = load_json_file(app_module.SCORES_FILE)
        self.assertEqual(len(scores), 1)
        user_id = list(scores.keys())[0]
        self.assertEqual(len(scores[user_id]), 1)

    # ---- Leaderboard ----

    def test_leaderboard_page_loads_without_login(self):
        response = self.client.get("/leaderboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Leaderboard", response.data)

    def test_leaderboard_ranks_by_best_score(self):
        # Create two users with different best scores and check ordering.
        self.login_as("Alice")
        self.client.post("/api/quiz-start", json={"mode": "normal"})
        # Answer all correct for Alice.
        with self.client.session_transaction() as sess:
            alice_id = sess["user_id"]
        for i, q in enumerate(app_module.active_quizzes[alice_id]["questions"]):
            self.client.post("/api/submit-answer",
                             json={"question_id": i, "answer": q["correct_answer"]})
        self.client.post("/api/submit-quiz", json={"time_taken": 100})
        self.client.get("/logout")

        self.login_as("Bob")
        self.client.post("/api/quiz-start", json={"mode": "normal"})
        # Bob answers nothing correctly.
        self.client.post("/api/submit-quiz", json={"time_taken": 100})
        self.client.get("/logout")

        response = self.client.get("/leaderboard")
        html = response.data.decode("utf-8")
        # Alice should appear before Bob.
        self.assertLess(html.index("Alice"), html.index("Bob"))

    # ---- Errors ----

    def test_404_page(self):
        response = self.client.get("/this-does-not-exist")
        self.assertEqual(response.status_code, 404)

    def test_submit_answer_with_bad_question_id(self):
        self.login_as("Ethan")
        self.client.post("/api/quiz-start", json={"mode": "normal"})
        response = self.client.post("/api/submit-answer",
                                    json={"question_id": -1, "answer": "x"})
        data = response.get_json()
        self.assertFalse(data["success"])


class JSONFileTestCase(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_save_and_load_roundtrip(self):
        path = os.path.join(self.test_dir, "test.json")
        data = {"name": "Ethan", "score": 42}
        save_json_file(path, data)
        self.assertEqual(load_json_file(path), data)

    def test_load_missing_file_returns_empty_dict(self):
        self.assertEqual(load_json_file(os.path.join(self.test_dir, "nope.json")), {})

    def test_load_corrupted_file_returns_empty_dict(self):
        path = os.path.join(self.test_dir, "bad.json")
        with open(path, "w") as f:
            f.write("{ not valid json")
        self.assertEqual(load_json_file(path), {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
