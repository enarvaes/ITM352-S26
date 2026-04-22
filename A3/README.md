# Quiz Game Web Application

## ITM 352 - Assignment 3
**Name:** Ethan Narvaes
**Date:** April 21, 2026

This is a Flask web application version of the console quiz game from
Assignment 1. The user logs in with a name, answers a set of randomized
multiple-choice questions, sees feedback and an explanation after each
answer, and gets a final score page. Scores are saved so returning users
see their history on the dashboard, and the leaderboard ranks the top
10 players.

## Requirements Implemented

The assignment asked me to implement my two individual requirement numbers
from Assignment 1:
- Persistent User Identification and History (requirement 1)
- Leaderboard System (requirement 2)

For extra credit I also added:
- Answer Explanations (shown in a modal after each question)
- Responsive Design for Mobile (Bootstrap 5 + custom media queries)

The Timer Mode and Progress Bar extras are wired up in the templates but
turned off in `app.py` under `EXTRAS_ENABLED`. They can be flipped on by
changing that dict.

## How to Run

1. Make sure Python 3.8+ is installed.
2. From this folder, install Flask:

       pip install -r requirements.txt

3. Start the app:

       python app.py

4. Open `http://127.0.0.1:5000/` in a browser.

## How to Run the Tests

    python test_app.py

The tests use a temporary data folder, so running them will not touch the
real `data/users.json` or `data/scores.json`.

## Project Structure

    app.py              - Flask app, routes, and REST API
    test_app.py         - unittest test suite
    requirements.txt    - Python dependencies
    templates/          - Jinja HTML templates (login, dashboard, quiz, etc.)
    static/
        style.css       - custom CSS on top of Bootstrap
        main.js         - small shared helpers
    data/
        questions.json  - list of quiz questions (edit to change content)
        users.json      - auto-created, stores user profiles
        scores.json     - auto-created, stores quiz results

## Design Notes

The quiz questions get shuffled once per user when the quiz starts. The
shuffled list is kept in an in-memory dict (`active_quizzes`) so that
every API call during one quiz sees the same order. An earlier version
reshuffled on every API call, which meant "question 0" changed between
loading the question and submitting the answer - I found that while
writing tests and it was the main bug I had to fix.

Scores are computed on the server, not the client. The client tells the
server what was picked; the server looks up the correct answer and
records whether it was right. When the user submits the quiz, the server
adds up its own records to get the final score.

## REST API

| Method | Route                          | Purpose                                 |
|--------|--------------------------------|-----------------------------------------|
| POST   | /api/quiz-start                | Start a new quiz, return first question |
| GET    | /api/question/&lt;id&gt;       | Get a specific question by index        |
| POST   | /api/submit-answer             | Submit one answer, get feedback         |
| POST   | /api/submit-quiz               | Finish quiz, save score, return result  |

See `REQUIREMENTS_SATISFACTION.md` for how each assignment requirement is
covered. See `USE_OF_AI.md` for where I used AI help.
