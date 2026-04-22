# Requirements Satisfaction

**Name:** Ethan Narvaes
**Assignment:** ITM 352 Assignment 3

This document goes through each core requirement from the assignment
and explains where it is satisfied in the code.

## Core Requirements

### 1. User Interface

The UI is built with HTML templates (`templates/`) that extend a common
`base.html` layout. Bootstrap 5 is used for the layout grid, buttons,
cards, and modals. Custom CSS is in `static/style.css`. The quiz page
uses plain JavaScript (no framework) to load questions from the API
and show immediate feedback. The templates are: `login.html`,
`dashboard.html`, `quiz.html`, `results.html`, `leaderboard.html`,
`404.html`, and `500.html`.

### 2. Question Display

Questions are loaded from `data/questions.json` by `app.py` -
specifically the `start_new_quiz()` function on each new quiz. It reads
the JSON file, shuffles the question order with `random.shuffle()`,
then shuffles each question's options list, and caches the shuffled
copy for the user. Nothing is hard-coded in any template or route. To
add more questions, just add more entries to `data/questions.json` -
no code changes are needed.

### 3. Answer Submission and Feedback

The `/api/submit-answer` route in `app.py` takes a question id and the
user's answer, looks up the correct answer for that question in the
cached quiz, and returns a JSON object saying whether it was right,
what the correct answer is, and the explanation. The front-end
(`templates/quiz.html`) shows a green or red alert immediately and
pops open a modal with the explanation (when that extra is enabled).
A running "Answered: X/Total" count is shown in the header so the
user sees their progress.

### 4. Data Management

All persistent data is stored in JSON files in the `data/` folder:

- `questions.json` - the list of quiz questions
- `users.json` - user profiles, keyed by user id
- `scores.json` - each user's quiz history, keyed by user id

`load_json_file()` and `save_json_file()` in `app.py` handle reading
and writing. Both have try/except around them so a missing or corrupt
file does not crash the app.

### 5. Backend

The server is Flask (see `app.py`). The REST API endpoints under
`/api/` return JSON and are used by the quiz page via `fetch()`:

- `POST /api/quiz-start`
- `GET /api/question/<id>`
- `POST /api/submit-answer`
- `POST /api/submit-quiz`

The non-API routes (`/dashboard`, `/quiz`, `/results`, `/leaderboard`,
etc.) render HTML templates.

### 6. Score Tracking and Feedback

When the user finishes a quiz, `/api/submit-quiz` counts how many
answers the server recorded as correct, calculates a percentage score,
and appends a record to `scores.json` for that user. The record
includes the date, score, correct count, total, time taken, and mode.
The results page shows the final score, the correct/incorrect count,
the time taken, and a performance feedback message that changes
based on the score range. The dashboard shows total quizzes, average
score, best score, and the five most recent quiz results.

### 7. Error Handling and Validation

- The login route rejects names shorter than 2 characters and shows
  an error message on the login page.
- `/api/submit-answer` validates the question id is in range and
  returns `{success: false, error: ...}` if not.
- `/api/question/<id>` returns the same kind of error for an out-of-
  range id.
- The `load_json_file()` helper returns an empty dict/list if the
  file is missing or corrupt instead of crashing.
- 404 and 500 error handlers render friendly error pages.

## Non-Functional Requirements

**User-Friendliness.** The navigation is the same on every page
(Dashboard / Leaderboard / Logout in the top nav), forms have clear
labels, and errors appear as Bootstrap alert banners. The quiz page
gives immediate feedback after each answer instead of waiting until
the end.

**Documentation.** Setup and usage are in `README.md`. Inline comments
in `app.py` explain the trickier parts like why quiz state is cached
per user. This document covers each requirement.

**Performance.** All data is loaded from small local JSON files. The
quiz page only fetches one question at a time from the API, so the
initial page load is fast. The shuffled question list is cached in
memory per user so subsequent API calls during the same quiz don't
re-read the file.

**Quality Assurance.** `test_app.py` contains an automated test suite
using Python's built-in `unittest`. It covers the auth flow, each API
endpoint, the leaderboard ranking, data persistence, and the JSON
helpers. It runs against a temporary data directory so the tests do
not touch real user data.

**Maintainability.** Routes are grouped in `app.py` (page routes
first, then the API routes). Helper functions (`load_json_file`,
`save_json_file`, `start_new_quiz`, `get_active_quiz`) each do one
thing. The extras configuration is a single dict at the top of
`app.py` that controls which optional features are active, so
turning Timer Mode or the Progress Bar on or off is a one-line change.

## Individual Requirements

### Persistent User Identification and History

When the user submits the login form, `app.py` looks them up in
`users.json` by name (case-insensitive). If found, their `last_login`
is updated and their id is put in the Flask session. If not found, a
new user record is created. `PERMANENT_SESSION_LIFETIME` is set to 30
days so the session cookie sticks around between visits. On return,
the dashboard shows the user their total quiz count, average score,
best score, and last five quiz results from `scores.json`.

### Leaderboard System

The `/leaderboard` route reads every user's scores from `scores.json`,
computes each user's best and average score, sorts the list by best
score (with average as the tiebreaker), and passes the top 10 to
`templates/leaderboard.html`. If the current user is logged in and
ranked, their row is highlighted and their rank is shown at the top
of the page.

## Extra Credit

**Answer Explanations.** Each question in `questions.json` has an
`explanation` field. After the user submits an answer, the server
returns the explanation along with correctness, and `quiz.html` pops
open a Bootstrap modal with it.

**Responsive Design for Mobile.** The layout uses Bootstrap's
responsive grid (`col-md-*`) so cards stack on small screens.
`style.css` has extra `@media (max-width: 768px)` and `(max-width:
480px)` blocks that shrink headings, pad out buttons for touch, and
reduce the score circle size on phones.
