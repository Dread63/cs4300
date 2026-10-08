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
  reviewing my specs; making small spec edits I asked for; test-first implementation of each task
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
