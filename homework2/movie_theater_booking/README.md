# Movie Theater Booking

A RESTful movie theater booking app built with Django and Django REST Framework (DRF), for
CS 4300 Homework 2. Moviegoers can browse movies, see which seats are free, book a seat, and
check their booking history, through a Bootstrap web UI or a JSON API that share the same data
and the same booking rules.

**Live app (Render):** <https://REPLACE-WITH-YOUR-SERVICE.onrender.com>
**Demo account:** username `demo`. The password is in my Canvas submission comment.

---

## Features

| Feature | Web page | API |
|---|---|---|
| Movie listings | `/`: every movie, newest first, with release date, runtime and a **Book Now** button | `/api/movies/`: full CRUD |
| Seat booking | `/movies/<id>/seats/`: each seat shown as Available or Booked; **Book** when signed in, **Sign in to book** when not | `/api/seats/` (`?movie=<id>`), `POST /api/seats/<id>/book/` |
| Booking history | `/bookings/` (**My Bookings**): your bookings only, newest first | `/api/bookings/`: list, get one, create |
| Sign in / out | `/accounts/login/`, and a navbar button | — |

**Booking rules, the same everywhere.** Each seat belongs to one movie. A seat can be booked
once. The page, `/api/seats/<id>/book/` and `POST /api/bookings/` all call one model method,
`Seat.book(user)`. A taken seat is refused with *"Seat A2 is already booked"* (409 in the API),
even when two requests arrive at the same moment, because the database itself refuses a second
booking of a seat. A booking always belongs to the signed-in user, whatever the request says, and
nobody can see anyone else's bookings.

## API reference

All responses are JSON. Booking requires signing in (a session, from `/accounts/login/` or the
browsable API's "Log in" link).

| Method | URL | Who | Success | Errors |
|---|---|---|---|---|
| GET | `/api/movies/` | anyone | 200, list (newest first) | — |
| POST | `/api/movies/` | anyone | 201 | 400 (missing title or release date, duration ≤ 0) |
| GET / PUT / PATCH / DELETE | `/api/movies/<id>/` | anyone | 200 / 200 / 200 / 204 | 400, 404 |
| GET | `/api/seats/?movie=<id>` | anyone | 200, that movie's seats (`movie` is optional) | 400 if `movie` isn't a number |
| GET | `/api/seats/<id>/` | anyone | 200 | 404 |
| POST | `/api/seats/<id>/book/` | signed in | 201, the booking | 403, 404, **409** seat taken |
| GET | `/api/bookings/` | signed in | 200, **my** bookings, newest first | 403 |
| GET | `/api/bookings/<id>/` | signed in | 200 | 403; **404** if it isn't mine |
| POST | `/api/bookings/` with `{"seat": <id>}` | signed in | 201, the booking | 400 bad or missing seat, 403, **409** seat taken |
| PUT / PATCH / DELETE | `/api/bookings/<id>/` | — | — | 405 (bookings can't be changed) |

Movie create, update and delete are open to anyone. That's a deliberate scope decision in
[specs/001](specs/001-movie-listings/spec.md); restricting them to staff is out of scope.

## Project structure

```
movie_theater_booking/            ← this folder; run every command from here
├── manage.py
├── requirements.txt              ← pinned dependencies (Django, DRF, behave-django, coverage, gunicorn, whitenoise)
├── build.sh                      ← Render build: install, collectstatic, migrate, seed_demo
├── .python-version               ← Python 3.13, for Render
├── movie_theater_booking/        ← project settings and root URLs
│   ├── settings.py               ← reads SECRET_KEY / DEBUG / hosts from the environment on Render
│   └── urls.py                   ← admin/, accounts/ (sign in/out), and the bookings app
├── bookings/                     ← the app
│   ├── models.py                 ← Movie, Seat, Booking; Seat.book() holds the booking rules
│   ├── serializers.py            ← MovieSerializer, SeatSerializer, BookingSerializer
│   ├── views.py                  ← MovieViewSet, SeatViewSet, BookingViewSet + the three page views
│   ├── urls.py                   ← DRF router under api/, plus page routes
│   ├── admin.py                  ← Movie, Seat, Booking in the Django admin
│   ├── management/commands/seed_demo.py   ← demo movies, seats A1–A5, optional demo user
│   ├── migrations/
│   ├── templates/
│   │   ├── bookings/             ← base.html (Bootstrap 5, navbar), movie_list.html,
│   │   │                            seat_booking.html, booking_history.html
│   │   └── registration/login.html
│   └── tests.py                  ← 61 unit + integration tests
├── features/                     ← Behave (BDD) tests: 10 scenarios
│   ├── movie_listings.feature, seat_booking.feature, sign_in.feature, booking_history.feature
│   └── steps/
├── specs/                        ← spec-driven development: spec.md, plan.md, tasks.md per feature
│   ├── 001-movie-listings/
│   ├── 002-seat-booking/
│   └── 003-booking-history/
├── AI-USAGE.md                   ← detailed log of AI use (summary below)
├── AGENTS.md, CLAUDE.md          ← rules the AI assistant followed
├── SDD-GUIDE.md, prompts/        ← the course's SDD template guide and prompts
└── README.md
```

## Setup

Requires Python 3.12 or newer (developed on 3.13).

```bash
# from the homework2/ folder
python3 -m venv myenv --system-site-packages
source myenv/bin/activate
cd movie_theater_booking
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo          # 3 movies with seats A1–A5
python manage.py createsuperuser    # an account to sign in with, and for /admin/
```

`seed_demo` also creates a `demo` user if you set a password first:
`DEMO_PASSWORD=<choose one> python manage.py seed_demo`.

Seats and user accounts are created in the Django admin at `/admin/`. There is no sign-up page.

## Running the app

```bash
python manage.py runserver 0.0.0.0:3000
```

In DevEdu, click the **app** button next to the editor; its `app-*.devedu.io` address is
already allowed in `settings.py`. Locally, open <http://localhost:3000/>.

No environment variables are needed to run locally or in DevEdu. `DEBUG` is on, and a
development-only secret key is used.

## Running the tests

```bash
python manage.py test                                    # 61 unit + integration tests
python manage.py behave                                  # 10 Behave scenarios
coverage run --source=bookings manage.py test && coverage report --omit='bookings/migrations/*,bookings/tests.py'
```

Current results: all 61 tests and 10 scenarios (64 steps) pass, with **100% statement coverage**
of the `bookings` app.

- **Unit tests** cover model rules: ordering, seat numbers unique per movie, one booking per seat,
  and `Seat.book()`'s happy path, taken-seat case and race case.
- **Integration tests** call every API endpoint and page through Django's test client, checking
  status codes and JSON. They include the error paths: 400, 403, 404, 405, 409, and signed out.
  They also check that the page and both APIs refuse each other's bookings, and that one user
  never sees another's.
- **Behave scenarios** walk through the UI as a user: browse movies, follow **Book Now**, book a
  seat, hit a taken seat, sign in and come back, view My Bookings, and the empty states.

Every acceptance criterion in `specs/*/spec.md` maps to at least one named test. Each feature's
`tasks.md` lists them.

## Deployment (Render)

The app runs on a Render **Web Service** (free tier) with SQLite.

| Setting | Value |
|---|---|
| Root directory | `homework2/movie_theater_booking` |
| Build command | `./build.sh` |
| Start command | `gunicorn movie_theater_booking.wsgi:application` |
| Environment | `SECRET_KEY` (long random value), `DEMO_PASSWORD` (for the demo account) |

On Render, `settings.py` switches to production mode automatically. Render sets `RENDER` and
`RENDER_EXTERNAL_HOSTNAME`, so:
- `DEBUG` is off;
- the secret key must come from the environment;
- the Render hostname is allowed;
- HTTPS and secure cookies are enforced.

Static files (the admin's CSS and JS) are served by whitenoise.

**About the data:** the free tier has no persistent disk, so the SQLite database is rebuilt on
every deploy. `build.sh` re-runs migrations and `seed_demo`, so movies, seats and the demo
account always come back. Bookings made on the live site reset on the next deploy.

## How it was built

The app was built with **spec-driven development (SDD)**, using the course's
[SDD template](SDD-GUIDE.md). For each feature:
1. I made the design decisions in `spec.md` (user stories and Given/When/Then acceptance criteria).
2. A plan and an ordered task list were drafted and approved.
3. Each task was implemented **test first** (red → green → refactor) and committed on its own,
   which is why the history has one commit per task.

Notable decisions, with the reasons recorded in the specs:
- Seats belong to a movie, so availability is per movie.
- `Booking.seat` is one-to-one, so the database prevents double booking.
- A taken seat returns **409**, not 400.
- Someone else's booking returns **404**, not 403, so you can't tell whether it exists.
- A booking's user is always taken from the session, never from the request data.

## AI usage

Per the course policy, here's how AI was used. Details, task by task, are in
[AI-USAGE.md](AI-USAGE.md).

- **Tool:** Claude Code (Anthropic), model Claude Opus 5.5, run in VS Code. I used it in place of
  Codex with the course's SDD template; `CLAUDE.md` imports `AGENTS.md`, so it followed the same rules.
- **Used for:**
  - analyzing my project against the HW2 requirements;
  - downloading the SDD template;
  - setting up test tools and `requirements.txt`;
  - reviewing my specs and turning my spec decisions into acceptance criteria;
  - drafting plans and task lists for me to approve;
  - test-first implementation of each task: tests, models, viewsets, URLs, templates and Behave scenarios;
  - deployment configuration (`settings.py` environment handling, `build.sh`, `seed_demo`);
  - drafting this README.
- **How I used the output:**
  - I made the spec decisions (or approved the ones it proposed).
  - It implemented one task at a time and stopped. I read each diff, ran the tests, and committed
    each task myself.
  - I asked it why for anything I couldn't explain before committing.
