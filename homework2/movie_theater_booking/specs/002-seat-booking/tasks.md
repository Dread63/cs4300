# Tasks: Seat booking

**Plan:** [plan.md](plan.md)

> Each task is one small test-first increment and one commit: red → green → refactor when the behavior is missing,
> or a verification test if it already passes. Do them in order.
> Each task names its test and the acceptance criterion (AC-#) it covers.
> Codex ticks the box when the task's tests pass. **You** commit.

**Models: the booking rules live here (one place, AC-6)**
- [x] **T1** — `Seat.movie` FK, `seat_number` → CharField(4), unique (movie, seat number), ordering, `__str__` + migration · test: `test_seat_str_ordering_and_unique_number_per_movie` · covers: §4, AC-10
- [x] **T2** — `Booking.seat` → OneToOneField, `booking_date` auto, `__str__` + migration · test: `test_duplicate_booking_rejected_by_database` · covers: AC-4
- [x] **T3** — `SeatAlreadyBooked` + `Seat.book(user)`: creates the Booking (seat's movie, user, today) and sets status · test: `test_seat_book_creates_booking_and_sets_status` · covers: AC-2
- [x] **T4** — `book()` refuses a booked seat; nothing changes · test: `test_seat_book_taken_raises` · covers: AC-3
- [x] **T5** — `book()` turns the DB's `IntegrityError` into `SeatAlreadyBooked` (stale status, as if another request won the race) · test: `test_seat_book_race_raises_already_booked` · covers: AC-4

**API: `/api/seats/`**
- [x] **T6** — `SeatSerializer` + `movie`; read-only `SeatViewSet` + router; `?movie=` filter · tests: `test_list_seats_filtered_by_movie`, `test_list_all_seats` · covers: AC-10
- [x] **T6a** — `?movie=abc` → 400, not 500; `?movie=9999` → 200, empty · test: `test_list_seats_bad_movie_filter_400` · covers: AC-14
- [x] **T7** — `POST /api/seats/<id>/book/` → 201; `BookingSerializer` read-only `movie`/`user`/`booking_date` · test: `test_book_seat_via_api_201` · covers: AC-11
- [x] **T8** — Booking a taken seat via API → 409, including the race case · tests: `test_book_taken_seat_via_api_409`, `test_duplicate_booking_returns_error_not_500` · covers: AC-3, AC-4
- [x] **T9** — Signed out → 403; missing seat → 404 (GET and POST book) · tests: `test_book_via_api_signed_out_403`, `test_missing_seat_api_404` · covers: AC-8, AC-9
- [x] **T10** — `user` in request data is ignored · test: `test_booking_user_is_request_user_not_request_data` · covers: AC-5 (likely a verification test)

**Admin and sign-in**
- [x] **T11** — Register Movie, Seat, Booking in the admin · test: `test_admin_registers_models` · covers: Open Q (staff create seats)
- [x] **T12** — `django.contrib.auth.urls`, `registration/login.html`, redirect settings, navbar "Sign in" / "username · Sign out" · tests: `test_sign_in_and_out`, `test_sign_in_wrong_password` · covers: AC-12

**Seat booking page**
- [x] **T13** — `seat_booking` view + `book_seat` URL + template: seats with Available/Booked, extends `base.html` · tests: `test_seat_page_shows_available_and_booked`, `test_seat_booking_uses_base_template` · covers: AC-1, AC-7
- [x] **T14** — Missing movie → 404; movie with no seats → empty state · tests: `test_seat_page_missing_movie_404`, `test_seat_page_empty_state` · covers: AC-9, AC-13
- [x] **T15** — Signed out: available seats show "Sign in to book" · test: `test_signed_out_sees_sign_in_to_book` · covers: AC-8
- [x] **T16** — POST books via `Seat.book()`, redirects back, shows "Seat A1 booked for Dune" (messages in `base.html`) · tests: `test_book_seat_via_page`, `test_book_missing_seat_via_page_404` · covers: AC-2, AC-9
- [x] **T17** — POST on a taken seat shows "Seat A2 is already booked"; signed-out POST → sign-in page · tests: `test_book_taken_seat_via_page_shows_error`, `test_signed_out_post_redirects_to_login` · covers: AC-3, AC-8
- [x] **T18** — Page and API refuse each other's bookings · tests: `test_seat_booked_via_page_refused_via_seats_api`, `test_seat_booked_via_api_refused_via_page` · covers: AC-6 (likely verification tests)
- [ ] **T19** — "Book Now" on the movie list becomes a link to `book_seat`; update 001's Behave step for `<a>` · test: `test_movie_list_book_now_links_to_seat_page` · covers: AC-1

**Behave**
- [ ] **T20** — Scenarios "See seats for a movie" and "Browse seats signed out" · covers: AC-1, AC-8
- [ ] **T21** — Scenarios "Book an available seat" and "Seat already taken" · covers: AC-2, AC-3
- [ ] **T22** — Scenario "Sign in" · covers: AC-12

## Done when
- [ ] Every acceptance criterion in `spec.md` has a passing test
- [ ] Full suite green: `python manage.py test`
- [ ] `python manage.py behave` passes
- [ ] Coverage ≥ 80%
- [ ] `AI-USAGE.md` updated
