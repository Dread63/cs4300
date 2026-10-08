# Plan: Booking history

**Spec:** [spec.md](spec.md)   **Status:** Draft

> This says **how** the spec will be built. Codex drafts it (prompts/02-plan.md) and you approve it. Don't approve
> anything you can't explain.

## 1. Approach
The model is unchanged apart from a default order (AC-8).

**API.** `BookingViewSet` is built from DRF's `List`, `Retrieve` and `Create` mixins on a
`GenericViewSet`, with no update or destroy. The router then answers `PUT`/`PATCH`/`DELETE` with
405 by itself (AC-9).
- `permission_classes = [IsAuthenticated]` gives 403 when signed out (AC-6).
- `get_queryset()` returns only `request.user`'s bookings. List and retrieve both go through it, so
  another user's booking is a 404 (AC-2, AC-3). Privacy is enforced in the query, not in a template.

**Creating a booking.** The serializer validates `seat` (missing, not a number, unknown → 400).
`perform_create()` then calls **002's `Seat.book(request.user)`**, so the booking rules aren't built
twice (AC-7). `SeatAlreadyBooked` becomes a 409 through a small `SeatTaken` `APIException`.
002's `/api/seats/<id>/book/` switches to raise the same exception, so both endpoints share one
409 response.

**Page.** The My Bookings page is a `@login_required` function view, like 001 and 002's views.

**Rejected:**
- **A full `ModelViewSet` with `update`/`destroy` overridden to return 405.** It's more code to
  disable things than to leave them out.
- **Letting `ModelSerializer.create()` save the booking.** It would skip `Seat.book()`, so it
  wouldn't set `booking_status` or turn the race into a 409. That breaks 002's AC-4 and AC-6.

> 📖 **Book:** [§11.2.1 A01: Broken Access Control](https://www.swebook.org/chapters/11-software-security/index.html#1121-a01-broken-access-control)

## 2. Data model
| Model | Field | Type | Constraints | Spec ref |
|---|---|---|---|---|
| Booking | — | `Meta.ordering = ["-booking_date", "-id"]` (+ migration) | newest first; same day → newest id first | AC-8 |
| Booking | all fields | unchanged from 002 | user is always `request.user`; movie comes from the seat | AC-7 |

## 3. Endpoints / views
| Method | URL | View / ViewSet | Returns | Spec ref |
|---|---|---|---|---|
| GET | `/api/bookings/` | `BookingViewSet.list`: `get_queryset()` returns only `request.user`'s bookings | 200 list / 403 | AC-2, AC-6, AC-8 |
| GET | `/api/bookings/<id>/` | `BookingViewSet.retrieve`: same filtered queryset | 200 / **404** (not mine or no such booking) / 403 | AC-3, AC-6 |
| POST | `/api/bookings/` `{"seat": id}` | `BookingViewSet.create` → `perform_create()` → `Seat.book(request.user)` | 201 / 400 / 403 / 409 | AC-6, AC-7 |
| PUT/PATCH/DELETE | `/api/bookings/<id>/` | not provided (no update/destroy mixins) | 405 | AC-9 |
| GET | `/bookings/` (named `booking_history`) | `booking_history` view (`@login_required`) → `booking_history.html` | HTML / redirect to sign-in | AC-1, AC-2, AC-4–AC-6, AC-8 |

## 4. Files to create / change
| File | Change |
|---|---|
| `bookings/models.py` | `Booking.Meta.ordering` |
| `bookings/migrations/0006_…py` | generated |
| `bookings/serializers.py` | `BookingSerializer`: `extra_kwargs = {"seat": {"validators": []}}`, so a taken seat reaches `Seat.book()` and gets 409, not DRF's automatic 400 (see Risks) |
| `bookings/views.py` | `SeatTaken(APIException)` with status 409; `BookingViewSet`; `SeatViewSet.book` raises `SeatTaken` instead of building its own 409; `booking_history` view |
| `bookings/urls.py` | register `bookings` (`basename="booking"`); `bookings/` named `booking_history` |
| `bookings/templates/bookings/booking_history.html` | new: table of movie, seat, date (`M j, Y`); empty state with a link to Movies |
| `bookings/templates/bookings/base.html` | "My Bookings" navbar link, only when signed in |
| `features/booking_history.feature`, `features/steps/history_steps.py` | Behave scenarios, reusing 002's steps (sign in, seats, book) |
| `bookings/tests.py` | API and view tests below |

## 5. Test strategy
| Spec ref | Test type | Test name / scenario |
|---|---|---|
| AC-1 | view + Behave | `test_booking_history_shows_movie_seat_and_date`; "See my bookings" |
| AC-2 | API + view | `test_list_bookings_only_returns_own`, `test_booking_history_page_only_shows_own` |
| AC-3 | API | `test_retrieve_own_booking`, `test_cannot_retrieve_another_users_booking` (404) |
| AC-4 | view | `test_booking_history_uses_base_template`, `test_navbar_my_bookings_only_when_signed_in` |
| AC-5 | view + Behave | `test_booking_history_empty_state`; "No bookings yet" |
| AC-6 | view + API | `test_booking_history_signed_out_redirects_to_login`, `test_bookings_api_signed_out_403` (GET and POST) |
| AC-7 | API | `test_create_booking_201`, `test_create_booking_taken_seat_409`, `test_create_booking_bad_seat_400` (missing, `"abc"`, 9999), `test_create_booking_ignores_user_in_request_data`, `test_seat_booked_via_seats_api_refused_via_bookings_api` |
| AC-8 | unit + API + view | `test_booking_ordering_newest_first` (backdates one booking with `.update()`, since `booking_date` is set automatically); order also asserted in `test_list_bookings_only_returns_own` and `test_booking_history_page_only_shows_own` |
| AC-9 | API | `test_bookings_cannot_be_changed_or_deleted_405` |
| 002 AC-3 | API (regression) | 002's `test_book_taken_seat_via_api_409` must still pass after `book` switches to `SeatTaken` |

## 6. Risks & decisions
- **Filter in `get_queryset()`, not only in the template or the list view.** Otherwise
  `/api/bookings/<id>/` would still expose other users' bookings. Every detail lookup goes through
  `get_queryset()`, so a filtered queryset makes 404 the answer for anyone else's id.
- **DRF's automatic `UniqueValidator` on `seat`.** `Booking.seat` is a `OneToOneField`, so
  `ModelSerializer` adds a uniqueness check that runs before `perform_create()`. A taken seat would
  get **400** "booking with this seat already exists" instead of AC-7's **409**, and that check
  would sit outside `Seat.book()`. `extra_kwargs = {"seat": {"validators": []}}` removes it. The
  database constraint and `book()` still guarantee one booking per seat.
  `test_create_booking_taken_seat_409` catches it if this is removed.
- **`perform_create()` sets `serializer.instance`** to the booking `book()` returned, instead of
  calling `serializer.save()`. DRF's `create()` then responds with that booking's data.
- **Unknown seat is 400, not 404.** The seat comes in the request body, not the URL, so it's
  invalid input. That's DRF's standard answer for an unknown primary key in a body field.
- **The page and the API filter by user separately.** Each is one `.filter(user=request.user)`
  line. A shared helper would be more code than it saves.
- **No N+1 queries.** The page uses `select_related("movie", "seat")`, so a history of 20
  bookings runs one query instead of 41.
