# Use of AI

**Name:** Ethan Narvaes
**Assignment:** ITM 352 Assignment 3
**AI tool:** Claude (Anthropic)

I used Claude as a reference and to help debug. I did not have it build
the whole app for me. This document says where I used AI help and what
I changed.

## Where I asked for help

**Flask basics.** I had not used Flask before, so I asked Claude to
explain how routing, `render_template`, and the `session` object work.
I wrote my own routes based on that explanation.

**The login_required decorator.** The `login_required` decorator in
`app.py` is the standard Flask pattern. I copied the shape from Claude
and I understand how it works: it wraps a route, checks for
`session["user_id"]`, and redirects to `/login` if it is missing. That
function has a comment in the code marking that it was AI-assisted.

**Bootstrap class names.** When I wanted the score to show as a
colored pill, I asked Claude which Bootstrap badge classes to use. I
wrote the template Jinja myself; the only thing from Claude was things
like `badge bg-warning text-dark`.

**Test structure.** I asked Claude how to use `unittest` with Flask's
`test_client()`. I wrote my own tests based on the examples. The tests
also include a temp-directory setUp that I added after I realized the
first version of my tests was writing to the real `users.json` file.

**Debugging the shuffle bug.** I had a bug where submitted answers
did not match the correct answer shown. I described the symptom to
Claude and it pointed out that `load_questions()` was reshuffling on
every API call. I fixed this myself by moving the shuffle into
`start_new_quiz()` and caching the result per user in `active_quizzes`.

**CSS gradients.** The purple-to-blue gradient on buttons and the
score circle came from a CSS snippet Claude suggested. I adjusted the
colors and the border radius.

## Where I did NOT use AI

- The overall structure of `app.py` and which routes to have.
- The `questions.json` content (I wrote the questions and explanations).
- The `EXTRAS_ENABLED` dict pattern - this is my own idea so I could
  keep the optional features in the templates but turn them off in
  one place.
- The REST API shape (what the endpoints return, what the quiz page
  sends them).
- The `active_quizzes` cache for per-user quiz state.

## Things AI wrote that I removed

When I first asked Claude for a "full Flask quiz app" it gave me back
a very long `app.py` with docstrings on every single function, banner
comments like `# ========== ROUTES ==========`, an `Analytics` class
with `trackEvent()` and `trackPageView()` methods that only called
`console.log`, a `debounce` helper, a `throttle` helper, and cookie
helpers that weren't used anywhere. I removed all of that - the class
and the helpers were dead code, and the banners and heavy docstrings
did not match how I write Python in this class.

I also had AI generate a bunch of extra markdown files
(`API_DOCUMENTATION.md`, `GRADING_VERIFICATION.md`, a completion
checklist, a "formatting alignment" doc). I deleted them because the
assignment only asked for requirements satisfaction, a use-of-AI doc,
and the code itself - the rest was just padding.

## What I learned

The main thing I took away is that asking for small targeted pieces
works much better than "build me the whole thing". When I asked for
everything at once I got a lot of code I didn't understand and code
I didn't need. When I asked for one function at a time or one concept
at a time (like "how do Flask sessions work"), I could actually follow
what was happening and I wrote better code overall.
