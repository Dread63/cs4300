# AI Usage Log

Course policy: any use of AI (for ideas, text, code or anything else) must be cited in your
README, saying **which tool**, **what it was used for**, and **how you used the output**.
Keep this log as you go, then copy the summary into your README.

> 📖 **Book:** "Record where you used AI and how you verified it", [§13.2.10](https://www.swebook.org/chapters/13-ai-across-the-lifecycle/index.html#13210-the-team-project-appendix-a).

## Summary (paste into README)
- **Tool:** Claude Code (Anthropic), model: Claude Opus 5.5, run in VS Code. I used it in place of
  Codex with the same SDD template; `CLAUDE.md` imports `AGENTS.md` so it follows the same rules.
- **Used for:** analyzing where my project stood against the HW2 requirements; downloading the SDD
  template; installing test tools (`coverage`, `behave-django`) and writing `requirements.txt`;
  reviewing my specs; making small spec edits I asked for; turning my spec decisions into
  acceptance criteria; drafting plans and task lists for me to approve; test-first implementation of each task
  (tests, models, viewsets, URLs, templates, Behave scenarios); splitting my uncommitted work into
  one commit per task.
- **How I used the output:** I made the spec decisions (or approved the ones it proposed). It
  implemented one task at a time and stopped; I read each diff, ran the tests, and committed each
  task myself. I asked it why for anything I couldn't explain before committing.

## Log
| Date | Feature / task | What I asked the AI | What I kept, changed or rejected |
|---|---|---|---|
| 2026-10-08 | Setup | Analyze my repo against the HW2 PDF and estimate remaining time | Kept the gap list and order of work; I hadn't started views, URLs, templates, tests or deployment |
| 2026-10-08 | Setup | Download the SDD template; install coverage + behave-django; add `behave_django` to `INSTALLED_APPS`; write `requirements.txt`; add `CLAUDE.md` | Kept all of it. It caught that Django was missing from `pip freeze --local` (system site-packages) and added it by hand |
| 2026-10-08 | 001 spec | Prompt 1 review of the 001 spec, then make the minimum valuable edits | Kept: exact AC-3 format (`Oct 22, 2021`, `155 min`), `<button disabled>` in AC-1, new AC-10 (newest first), answered the required-fields question. My editor overwrote some edits once; it restored them and kept my header |
| 2026-10-08 | 001 T1 | Movie `__str__`, ordering, optional description (test first) | Kept. Also changed `description` from `CharField(200)` to `TextField(blank=True)` to match the spec |
| 2026-10-08 | 001 T2–T5 | `MovieViewSet` + router; create, missing-title and missing-date tests | Kept. T3–T5 were verification tests: `ModelViewSet`/`ModelSerializer` already did the work. T2 also fixed broken `views.py` |
| 2026-10-08 | 001 commits | Commit T1–T4 for me (I'd committed in the wrong repo) | Kept: it split the work into one commit per task and ran the tests at each one |
| 2026-10-08 | 001 T6 | Reject duration ≤ 0 | Kept. Real red → green: `PositiveIntegerField` allows 0, so it added `MinValueValidator(1)` on the model and updated the plan to match |
| 2026-10-08 | 001 T7–T10 | Retrieve, 404, PUT/PATCH, delete tests | Kept; all verification tests |
| 2026-10-08 | 001 T11–T13 | `base.html` (Bootstrap + navbar), `movie_list` view/template, date/duration, empty state | Kept |
| 2026-10-08 | 001 T14–T15 | Behave scenarios for AC-1 and AC-2 | Kept. 13 unit tests + 2 scenarios pass; 100% coverage of `bookings` |
| 2026-10-08 | 002 spec | Ask me the key decisions, then write them into the 002 spec | I chose: seats belong to a movie; text seat numbers like "A1"; taken seat = API 409 + page error; signed out can view but must sign in to book. It filled in the remaining TODOs as defaults (stay on the page after booking, `/api/seats/<id>/book/`, built-in sign-in with admin-created accounts, AC-8/9/12/13) for me to override |
| 2026-10-08 | 002 plan | Prompt 2: draft the plan | Approved as drafted: `Seat.movie`, `Booking.seat` as `OneToOneField`, one shared `Seat.book()` model method (rejected: rules in the serializer, which would duplicate them for the page) |
| 2026-10-08 | 002 tasks | Prompt 3: break the plan into tasks | Kept 22 tasks, models → API → admin/sign-in → page → Behave |
| 2026-10-08 | 002 T1–T5 | Seat/Booking model changes and `Seat.book()`: happy path, taken seat, race | Kept. Each was a real red → green; T4 showed the raw `IntegrityError` before the check, T5 caught it and re-raised `SeatAlreadyBooked` |
| 2026-10-08 | 002 T6, T6a | `/api/seats/` with `?movie=` filter | Kept. It found that `?movie=abc` returned 500 and put it in Open Questions instead of fixing it silently; I chose 400, which became AC-14 |
| 2026-10-08 | 002 T7–T10 | `book` action: 201, 409 (incl. race), 403 signed out, 404, user ignored | Kept. T9 fixed a 500 for signed-out POSTs that T7 left open (and flagged); T10 was a verification test |
| 2026-10-08 | 002 T11–T12 | Admin registration; sign in/out with Django's auth views | Kept |
| 2026-10-08 | 002 T13–T19 | Seat booking page: availability, 404/empty state, sign-in link, booking form, errors, page ↔ API cross-checks, real "Book Now" link | Kept. In T16 it probed bad input and found junk `seat` values crashed the page (500); fixed to 404 per spec §5 and added the test to the plan. T19 broke a 001 Behave step, as the plan predicted, and it updated the step |
| 2026-10-08 | 002 T20–T22 | Behave scenarios for AC-1, 2, 3, 8, 12 | Kept. It wrote a bogus placeholder line in one step and replaced it before running. 42 unit tests + 8 scenarios pass; 100% coverage of `bookings` |
| 2026-10-08 | 003 spec | Ask me the key decisions, then write them into the 003 spec | I chose: someone else's booking = 404 (doesn't leak that it exists); signed out → sign-in page / API 403; create with just `{"seat": id}`; newest first. It filled in defaults (empty state, 405 for edit/delete as AC-9, staff only see everyone's bookings in the admin) for me to override |
| 2026-10-08 | 003 plan | Prompt 2: draft the plan | Approved. It checked DRF and found the automatic `UniqueValidator` on the one-to-one `seat` field would answer a taken seat with 400 instead of my 409, and planned to remove it |
| 2026-10-08 | 003 tasks | Prompt 3: break the plan into tasks | Kept 14 tasks |
| 2026-10-08 | 003 T1–T5 | Ordering; user-scoped `BookingViewSet` (list, retrieve, create via `Seat.book()`); taken seat → 409 | Kept. T3 was predicted to be a verification test but was a real red → green (no detail route existed yet). T5 hit the predicted 400, then removed the validator and added a shared `SeatTaken` 409 used by both booking endpoints |
| 2026-10-08 | 003 T6–T9 | Bad seat 400, `user` ignored, signed out 403, edit/delete 405 | Kept; all verification tests (the serializer field, `read_only_fields`, `IsAuthenticated` and the chosen mixins already did the work) |
| 2026-10-08 | 003 T10–T13 | My Bookings page, empty state, `@login_required`, navbar link | Kept. It flagged that the page crashed when signed out until T12 added `@login_required` |
| 2026-10-08 | 003 T14 | Behave scenarios for AC-1 and AC-5 | Kept. 59 unit tests + 10 scenarios pass; 100% coverage of `bookings` |
| 2026-10-08 | Deployment prep | Prepare the repo for Render | Kept: `settings.py` reads `SECRET_KEY`/`DEBUG`/hosts from the environment on Render (unchanged locally and in DevEdu), HTTPS + secure cookies on Render, whitenoise for static files, `build.sh`, `.python-version`, a tested `seed_demo` command (demo password from an env var, not code), untracked `db.sqlite3`. It rehearsed the build and gunicorn start locally, including a sign-in POST through a simulated HTTPS proxy, before I deployed. It silenced Django 6.1's email deploy check because the app sends no email, and left HSTS off on purpose |
| 2026-10-08 | README | Draft the project README | Kept the structure; I filled in the Render URL after deploying. Renamed the SDD template's README to `SDD-GUIDE.md` |
