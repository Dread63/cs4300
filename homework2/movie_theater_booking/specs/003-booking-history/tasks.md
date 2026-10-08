# Tasks: Booking history

**Plan:** [plan.md](plan.md)

> Each task is one small test-first increment and one commit: red → green → refactor when the behavior is missing,
> or a verification test if it already passes. Do them in order.
> Each task names its test and the acceptance criterion (AC-#) it covers.
> Codex ticks the box when the task's tests pass. **You** commit.

**Model**
- [x] **T1** — `Booking.Meta.ordering` newest first + migration · test: `test_booking_ordering_newest_first` · covers: AC-8

**API: `/api/bookings/`**
- [x] **T2** — `BookingViewSet` (list) + router + `IsAuthenticated`; `get_queryset()` is only my bookings · test: `test_list_bookings_only_returns_own` (also checks newest first) · covers: AC-2, AC-8
- [x] **T3** — Retrieve: mine → 200, someone else's → 404 · tests: `test_retrieve_own_booking`, `test_cannot_retrieve_another_users_booking` · covers: AC-3
- [x] **T4** — Create: `POST {"seat": id}` → 201 via `Seat.book(request.user)` in `perform_create()` · test: `test_create_booking_201` · covers: AC-7
- [x] **T5** — Taken seat → 409: `SeatTaken` exception, drop DRF's auto `UniqueValidator` on `seat`; `/api/seats/<id>/book/` raises `SeatTaken` too · tests: `test_create_booking_taken_seat_409`, `test_seat_booked_via_seats_api_refused_via_bookings_api` (+ 002's `test_book_taken_seat_via_api_409` still green) · covers: AC-7
- [ ] **T6** — Bad seat → 400: missing, `"abc"`, 9999 · test: `test_create_booking_bad_seat_400` · covers: AC-7 (likely verification)
- [ ] **T7** — `user` in request data is ignored · test: `test_create_booking_ignores_user_in_request_data` · covers: AC-7 (likely verification)
- [ ] **T8** — Signed out → 403 for GET and POST · test: `test_bookings_api_signed_out_403` · covers: AC-6 (likely verification)
- [ ] **T9** — `PUT`/`PATCH`/`DELETE` → 405, booking unchanged · test: `test_bookings_cannot_be_changed_or_deleted_405` · covers: AC-9 (likely verification)

**My Bookings page**
- [ ] **T10** — `booking_history` view + `/bookings/` URL + template (movie, seat, date; only mine; newest first; extends `base.html`) · tests: `test_booking_history_shows_movie_seat_and_date`, `test_booking_history_page_only_shows_own`, `test_booking_history_uses_base_template` · covers: AC-1, AC-2, AC-4, AC-8
- [ ] **T11** — Empty state with a link to Movies · test: `test_booking_history_empty_state` · covers: AC-5
- [ ] **T12** — Signed out → sign-in page, then back (`@login_required`) · test: `test_booking_history_signed_out_redirects_to_login` · covers: AC-6
- [ ] **T13** — "My Bookings" navbar link, only when signed in · test: `test_navbar_my_bookings_only_when_signed_in` · covers: AC-4

**Behave**
- [ ] **T14** — Scenarios "See my bookings" (book a seat on the page, then open My Bookings) and "No bookings yet" · covers: AC-1, AC-5

## Done when
- [ ] Every acceptance criterion in `spec.md` has a passing test
- [ ] Full suite green: `python manage.py test`
- [ ] `python manage.py behave` passes
- [ ] Coverage ≥ 80%
- [ ] `AI-USAGE.md` updated
