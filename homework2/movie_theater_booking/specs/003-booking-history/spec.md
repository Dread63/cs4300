# Spec: Booking history

**Status:** Draft, decisions made, ready for review
**Author:** Joshua Douglas  **Date:** 2026-10-08

> The user stories (US-#) and first acceptance criteria (AC-#) are started for you. Every `TODO` is a decision **you** make.

## 1. Problem
Moviegoers need to see what they've booked. (Homework 2, or HW2, §1 "Check their booking history via the API";
§3.3 `BookingViewSet` "for users to book seats and view their booking history"; §3.5
`/api/bookings/`; template `booking_history.html`.)

## 2. User stories
- **US-1:** As a moviegoer, I want to see a list of my bookings, so that I know what I've reserved.
- **US-2:** As an API client, I want to view booking history and create bookings through `/api/bookings/`.
- **US-3:** As a moviegoer, I want my bookings kept private, so that other users can't see them.
- Bookings can't be changed or cancelled (002 Out of scope), so the history is read-only apart
  from creating a booking.

## 3. Acceptance criteria

**AC-1 (US-1): See my bookings**
- Given I am signed in and have booked seat A1 for "Dune"
- When I open My Bookings
- Then I see Dune, seat A1 and the booking date (in the same format as 001's dates, e.g. "Oct 8, 2026")

**AC-2 (US-1, US-3): Only my bookings**
- Given users Sam and Alex each have bookings
- When Sam opens My Bookings, or sends `GET /api/bookings/`
- Then only Sam's bookings appear, and none of Alex's

**AC-3 (US-3): Someone else's booking**
- Given Alex has a booking with id 7
- When Sam sends `GET /api/bookings/7/`
- Then the response is **404**, and none of Alex's booking data is returned
- (Why 404, not 403: to Sam, Alex's bookings don't exist. A 403 would confirm that booking 7 is
  real, which leaks information about other users. 404 is also what Sam gets for an id that
  doesn't exist at all, so the two cases can't be told apart.)

**AC-4 (UI): Consistent layout**
- Given the My Bookings page
- When it renders
- Then it extends `base.html`, and when I'm signed in the navbar links to both Movies and My Bookings
- (Signed out, the navbar shows Movies and Sign in only; see AC-6.)

**AC-5 (US-1): No bookings yet**
- Given I am signed in and have no bookings
- When I open My Bookings
- Then I see "You haven't booked any seats yet" and a link to the movie list

**AC-6 (US-3): Not signed in**
- Given I am not signed in
- When I open My Bookings
- Then I'm sent to the sign-in page, and after signing in I come back to My Bookings
- And `GET /api/bookings/` and `POST /api/bookings/` without signing in return **403**

**AC-7 (US-2): Create a booking via API, with the same rules as 002**
- Given I am signed in and Dune's seat A1 is available
- When a client sends `POST /api/bookings/` with `{"seat": <A1's id>}`
- Then the response is **201** with the new booking (id, movie, seat, user, booking date), the
  movie is Dune (taken from the seat), and A1 is now booked
- And if A1 was already booked (through the page, `/api/seats/` or `/api/bookings/`), the
  response is **409** with "Seat A1 is already booked", exactly as in 002's AC-3
- And if the request data names another user, the booking is still mine (002's AC-5)
- And if `seat` is missing, isn't a number, or no such seat exists, the response is **400** with
  an error for `seat`, and nothing is booked
- (This reuses 002's booking operation. The rule isn't built twice.)

**AC-8 (US-1, US-2): Newest first**
- Given I booked Up's seat A1 yesterday and Dune's seat A2 today
- When I open My Bookings, or send `GET /api/bookings/`
- Then the Dune booking comes first. Bookings made on the same day are newest first too.

**AC-9 (US-2): Bookings can't be edited or deleted through the API**
- Given I have a booking
- When a client sends `PUT`, `PATCH` or `DELETE` to `/api/bookings/<id>/`
- Then the response is **405**, and the booking is unchanged

## 4. Data
| Thing | Information | Rules |
|---|---|---|
| Booking | movie, seat, user, booking date | Only ever shown to its own user (AC-2, AC-3), even to staff, outside the admin. Never changed after it's made (AC-9). Same creation rules as 002 (AC-7) |

## 5. API / UI behavior
| Action | Input | Success result | Failure result |
|---|---|---|---|
| My Bookings page | signed-in user | my bookings, newest first: movie, seat, date | sign-in page if signed out |
| List bookings (API) | signed-in user | 200, my bookings, newest first | 403 signed out |
| Get one booking (API) | id | 200, my booking | 404 if not mine or no such booking; 403 signed out |
| Create booking (API) | `{"seat": id}` | 201, booking | 409 taken; 400 bad or missing seat; 403 signed out |
| Change or delete booking (API) | — | — | 405 |

## 6. Out of scope
- Cancelling or changing a booking (002 Out of scope)
- Staff seeing everyone's bookings in the API or on the page; the Django admin already shows them
- Paging or filtering the history

## 7. Open questions
- [x] AC-2 and AC-3 say users only see their own bookings. Why is this a **security** requirement,
      not just a feature choice? Could an admin or staff user ever see everyone's? If so, write that
      as its own AC. 📖 **Book:** [§11.2.1 A01: Broken Access Control](https://www.swebook.org/chapters/11-software-security/index.html#1121-a01-broken-access-control)
      → It's security because a booking ties a person to a time and a place. If any signed-in user
      could list or fetch others' bookings by changing an id, that's broken access control (OWASP A01),
      whatever the UI shows. So the rule is enforced on the server (the query only ever contains the
      signed-in user's bookings) and tested at the API, not just hidden in the page. **Staff see
      everyone's bookings only in the Django admin**; the page and the API treat staff like anyone
      else, so there's no extra AC.
- [x] Does a booking need its own time, or is the date enough for "newest first"? → **The date is
      enough.** Same-day bookings fall back to newest id first (AC-8), which is the order they were made.
