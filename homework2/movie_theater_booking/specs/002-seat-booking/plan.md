# Plan: Seat booking

**Spec:** [spec.md](spec.md)   **Status:** Approved

> This says **how** the spec will be built. Codex drafts it (prompts/02-plan.md) and you approve it. Don't approve
> anything you can't explain.

## 1. Approach
Each `Seat` gets a `movie` foreign key, and `Booking.seat` becomes a `OneToOneField`, so the
database itself refuses a second booking of a seat (AC-4). All booking goes through **one model
method, `Seat.book(user)`**. It runs in a transaction, refuses a seat that's taken by raising
`SeatAlreadyBooked`, creates the `Booking` (movie taken from the seat, user passed in by the
caller), and sets `booking_status = True`. Callers only translate the result:
- the seat booking page turns `SeatAlreadyBooked` into an error message;
- `SeatViewSet`'s `book` action turns it into **409**;
- 003's `BookingViewSet.create` will call the same method.

That's what makes AC-6 hold: there is one set of rules, not three copies.

The API is a `ReadOnlyModelViewSet` for seats, plus one `@action` for booking. Seats can't be
created or edited through the API (spec §6). The page is a plain Django view, like 001's
`movie_list`. It uses POST-then-redirect and Django's messages framework for "Seat A1 booked for
Dune". Sign-in uses Django's built-in auth views (`django.contrib.auth.urls`).

**Rejected:**
- **Putting the rules in `BookingSerializer.create()`.** The seat page doesn't use a serializer,
  so it would need its own copy of the rules, which breaks AC-6.
- **A separate `services.py` module.** It works just as well, but it's one more file for a
  single function. A model method keeps the rule next to the data it protects.

> 📖 **Book:** [§7.2.1 The Shared-Data Pattern](https://www.swebook.org/chapters/07-architectural-patterns/index.html#721-the-shared-data-pattern), [§11.2.1 Broken Access Control](https://www.swebook.org/chapters/11-software-security/index.html#1121-a01-broken-access-control)

## 2. Data model
| Model | Field | Type | Constraints | Spec ref |
|---|---|---|---|---|
| Seat | movie | ForeignKey → Movie | required; `on_delete=CASCADE`; `related_name="seats"` | §4, AC-1, AC-10 |
| Seat | seat_number | CharField (was PositiveIntegerField) | `max_length=4`; `UniqueConstraint(movie, seat_number)` | §4, AC-10 |
| Seat | booking_status | BooleanField (already exists) | `default=False`; **stored**, set only by `Seat.book()` | §4, Open Q |
| Seat | — | `Meta.ordering = ["seat_number"]`; `__str__` returns e.g. "Dune A1" | — | AC-10 |
| Seat | `book(user)` | method | `transaction.atomic()`; raises `SeatAlreadyBooked` if taken, including when the DB raises `IntegrityError` | AC-2–AC-6, AC-11 |
| Booking | seat | OneToOneField → Seat (was ForeignKey) | unique, so at most one booking per seat | AC-4 |
| Booking | movie | ForeignKey → Movie (already exists) | always set from `seat.movie` inside `book()` | §4 |
| Booking | user | ForeignKey → user model (already exists) | set from `request.user` on the server; read-only in the serializer | AC-5 |
| Booking | booking_date | DateField | `auto_now_add=True` (today, set automatically) | AC-2, §4 |
| Booking | — | `__str__` returns e.g. "sam: Dune A1" | — | admin readability |
| — | `SeatAlreadyBooked` | exception class in `models.py` | message "Seat A2 is already booked" | AC-3 |

## 3. Endpoints / views
| Method | URL | View / ViewSet | Returns | Spec ref |
|---|---|---|---|---|
| GET | `/movies/<movie_id>/seats/` (named `book_seat`) | `seat_booking` view → `seat_booking.html` | HTML / 404 | AC-1, AC-7, AC-8, AC-9, AC-13 |
| POST | `/movies/<movie_id>/seats/` (form field `seat`) | `seat_booking` view → `Seat.book()` → redirect back with a message | 302 / 404; sign-in page if signed out | AC-2, AC-3, AC-5, AC-6, AC-8 |
| GET/POST | `/accounts/login/`, POST `/accounts/logout/` | Django's `LoginView` / `LogoutView` via `include("django.contrib.auth.urls")` | HTML / 302 | AC-12 |
| GET | `/api/seats/` and `?movie=<id>` | `SeatViewSet.list` (`get_queryset` filters by `movie`) | 200 list | AC-10 |
| GET | `/api/seats/<id>/` | `SeatViewSet.retrieve` | 200 / 404 | AC-9 |
| POST | `/api/seats/<id>/book/` | `SeatViewSet.book` (`@action`, `IsAuthenticated`) → `Seat.book()` | 201 booking / 409 / 403 / 404 | AC-3, AC-5, AC-6, AC-8, AC-9, AC-11 |

## 4. Files to create / change
| File | Change |
|---|---|
| `bookings/models.py` | `Seat.movie`, `seat_number` → CharField, constraint, ordering, `__str__`, `book()`; `SeatAlreadyBooked`; `Booking.seat` → OneToOneField; `booking_date` → `auto_now_add`; `Booking.__str__` |
| `bookings/migrations/0004_…py` | generated. `makemigrations` will ask for a one-off default for `Seat.movie`. The table is empty, so any movie id works and nothing uses it |
| `bookings/serializers.py` | `SeatSerializer` adds `movie`; `BookingSerializer` makes `movie`, `user` and `booking_date` read-only |
| `bookings/views.py` | `SeatViewSet` (+ `book` action); `seat_booking` view |
| `bookings/urls.py` | register `seats`; `movies/<int:movie_id>/seats/` named `book_seat` |
| `bookings/admin.py` | register Movie, Seat, Booking, because staff create seats and users here (spec Open Q) |
| `movie_theater_booking/urls.py` | `path("accounts/", include("django.contrib.auth.urls"))` |
| `movie_theater_booking/settings.py` | `LOGIN_REDIRECT_URL = LOGOUT_REDIRECT_URL = "movie_list"` |
| `bookings/templates/bookings/base.html` | navbar "Sign in" link or "username · Sign out" (a POST form); show `messages` as Bootstrap alerts |
| `bookings/templates/bookings/seat_booking.html` | new: seats with Available/Booked badges; "Book" form per available seat, or a "Sign in to book" link; empty state |
| `bookings/templates/registration/login.html` | new: sign-in form; Django's auth views look for this exact path |
| `bookings/templates/bookings/movie_list.html` | turn 001's disabled "Book Now" into `{% url 'book_seat' movie.id %}` |
| `features/steps/movie_steps.py` | 001's "Book Now" step looks for a `<button>`, so it must accept the new `<a>` |
| `features/seat_booking.feature`, `features/steps/seat_steps.py` | new Behave scenarios |
| `bookings/tests.py` | model, API and view tests below |

## 5. Test strategy
| Spec ref | Test type | Test name / scenario |
|---|---|---|
| §4 | unit | `test_seat_str_ordering_and_unique_number_per_movie` |
| AC-1 | view + Behave | `test_seat_page_shows_available_and_booked`, `test_movie_list_book_now_links_to_seat_page`; "See seats for a movie" |
| AC-2 | unit | `test_seat_book_creates_booking_and_sets_status` |
| AC-2 | view + Behave | `test_book_seat_via_page` (redirect, message, Booking row, status, date); "Book an available seat" |
| AC-3 | unit | `test_seat_book_taken_raises` |
| AC-3 | view + API + Behave | `test_book_taken_seat_via_page_shows_error`, `test_book_taken_seat_via_api_409`; "Seat already taken" |
| AC-4 | unit | `test_seat_book_race_raises_already_booked` (stale status; the DB refuses; `SeatAlreadyBooked` is raised) |
| AC-4 | unit | `test_duplicate_booking_rejected_by_database` (a second `Booking` for the same seat raises `IntegrityError`) |
| AC-4 | API | `test_duplicate_booking_returns_error_not_500` (a booking exists but the status still says available, as if another request won the race; the response is 409, not 500) |
| AC-5 | API | `test_booking_user_is_request_user_not_request_data` |
| AC-6 | view + API | `test_seat_booked_via_page_refused_via_seats_api`, `test_seat_booked_via_api_refused_via_page` |
| AC-7 | view | `test_seat_booking_uses_base_template` |
| AC-8 | view + API + Behave | `test_signed_out_sees_sign_in_to_book`, `test_signed_out_post_redirects_to_login`, `test_book_via_api_signed_out_403`; "Browse seats signed out" |
| AC-9 | view + API | `test_seat_page_missing_movie_404`, `test_missing_seat_api_404` (GET and POST book) |
| AC-10 | API | `test_list_seats_filtered_by_movie`, `test_list_all_seats` |
| AC-11 | API | `test_book_seat_via_api_201` |
| AC-12 | view + Behave | `test_sign_in_and_out`, `test_sign_in_wrong_password`; "Sign in" |
| AC-13 | view | `test_seat_page_empty_state` |
| Open Q | unit | `test_admin_registers_models` |

## 6. Risks & decisions
- **Double booking is a race.** `book()` checks `booking_status` first, so it can give the friendly
  error. That check alone is race-prone: two requests can both see "available" before either one
  saves. The `OneToOneField` is what actually guarantees AC-4. The `IntegrityError` it raises is
  caught inside `book()`'s transaction and re-raised as `SeatAlreadyBooked`. Because the whole
  transaction rolls back, a losing request never sets the status, and the client gets a 409, never
  a 500. (SQLite ignores `select_for_update()`, so it isn't used. The constraint is the guarantee
  on every database.)
- **Never trust the client for `user`.** It is set from `request.user` (AC-5). `user` is
  read-only in `BookingSerializer`, and `POST /api/seats/<id>/book/` reads no body at all. A `user`
  value in the request is therefore **ignored**: the client gets 201 with the signed-in user.
- **Status and Booking stay consistent** because only `book()` writes `booking_status`, inside the
  same transaction as the `Booking`. Cancellation is out of scope, so there's no second writer.
  Risk: staff could tick or untick `booking_status` in the admin. It's acceptable for HW2; the
  Booking table remains the source of truth, and the `OneToOneField` still blocks a duplicate.
- **403, not 401, when signed out.** DRF's default authentication tries `SessionAuthentication`
  first, and that doesn't send a `WWW-Authenticate` header, so DRF answers 403. The test pins this.
- **Sign-out must be a POST.** Django 5+ removed GET logout, so the navbar uses a small form.
- **Seat-number ordering is alphabetical**, so "A10" would sort before "A2". It's fine for A1–A9.
  Natural sort is out of scope.
- **001's Behave step changes.** "Book Now" becomes a link, so the step that looks for a `<button>`
  is updated in the same task. Behave catches that regression if it's missed.
