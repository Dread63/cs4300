# Spec: Seat booking

**Status:** Implemented
**Author:** Joshua Douglas  **Date:** 2026-10-08

> The user stories (US-#) and first acceptance criteria (AC-#) are started for you. Every `TODO` is a decision **you**
> make. Compare with `001-movie-listings/spec.md` for the level of detail to aim for.

## 1. Problem
A moviegoer who has picked a movie needs to see which seats are free and reserve one.
(Homework 2, or HW2, §1 "Book seats via the API"; §3.3 `SeatViewSet` "for seat availability and booking";
§3.5 `/api/seats/`; template `seat_booking.html`.)

## 2. User stories
- **US-1:** As a moviegoer, I want to see which seats are available for a movie, so that I can choose one.
- **US-2:** As a moviegoer, I want to book an available seat, so that it's reserved for me.
- **US-3:** As an API client, I want to check seat availability and book seats through `/api/seats/`.
  (HW2 also has `/api/bookings/` create bookings; see AC-6 and feature 003.)
- **US-4:** As a moviegoer, I want to sign in, so that my bookings are mine.
- One seat per booking. To book two seats, book twice.

## 3. Acceptance criteria

**AC-1 (US-1): Seat availability page**
- Given the movie "Dune" and seats A1–A5, where A2 is already booked
- When I click "Book Now" for Dune
- Then I see the seat booking page for Dune, with A2 shown as unavailable and the others as available
- (This is where "Book Now" on the movie list, disabled in 001, becomes a real link.)

**AC-2 (US-2): Book an available seat**
- Given I am signed in and seat A1 is available for Dune
- When I book A1
- Then I stay on Dune's seat booking page and see "Seat A1 booked for Dune", with A1 now shown
  as unavailable
- And one booking exists for A1 with me as the user, Dune as the movie and today as the booking
  date, and A1's booking status is "booked"

**AC-3 (US-2): Seat already taken**
- Given seat A2 is already booked for Dune
- When I try to book A2
- Then on the page I stay on Dune's seat booking page and see "Seat A2 is already booked"
- And through the API the response is **409 Conflict** with that message
- And nothing changes: A2 still has exactly one booking, the original one

**AC-4 (US-2): No double booking, even at the same moment**
- Given seat A1 is available for Dune
- When two requests to book A1 for Dune arrive at the same moment, or code saves a second booking
  of A1 for Dune without going through the page or API checks
- Then only one booking of A1 for Dune exists. The second save is refused, and a user or client
  making the second request gets the same answer as AC-3 (never a 500 error)
- (Checking "is it taken?" before saving isn't enough: two requests can both pass the check before
  either one saves. The database itself has to refuse the duplicate.)
- 📖 **Book:** the data store owns integrity constraints and concurrency control, [§7.2.1 The Shared-Data Pattern](https://www.swebook.org/chapters/07-architectural-patterns/index.html#721-the-shared-data-pattern).

**AC-5 (US-2, US-3): The booking belongs to whoever is signed in**
- Given I am signed in as Sam
- When I book a seat through the page or the API, even if the request data names another user
- Then the booking's user is Sam
- 📖 **Book:** [§11.2.1 A01: Broken Access Control](https://www.swebook.org/chapters/11-software-security/index.html#1121-a01-broken-access-control)

**AC-6 (US-2, US-3): Same rules everywhere**
- Given seat A1 has been booked for Dune through the seat booking page
- When anyone tries to book A1 for Dune through `/api/seats/` (or the other way round)
- Then it is refused exactly as in AC-3, because both follow one set of booking rules
- (003 adds `/api/bookings/` as a third way to book. It must follow the same rules: 003's AC-7.)

**AC-7 (UI): Consistent layout**
- Given the seat booking page for a movie
- When it renders
- Then it extends `base.html`, with the same navbar as the movie list

**AC-8 (US-1, US-4): Not signed in**
- Given I am not signed in
- When I open Dune's seat booking page
- Then I can see which seats are available, and each available seat's "Book" button says
  "Sign in to book" and takes me to the sign-in page
- And `POST /api/seats/<id>/book/` without signing in returns **403** and creates no booking

**AC-9 (US-1, US-3): Missing movie or seat**
- Given no movie with id 9999 and no seat with id 9999 exist
- When I open the seat booking page for movie 9999, or a client sends `GET /api/seats/9999/`
  or `POST /api/seats/9999/book/`
- Then each response is **404**, and no booking is created

**AC-10 (US-3): List and check seats via API**
- Given Dune has seats A1–A3 where A2 is booked, and Up has seat A1
- When a client sends `GET /api/seats/?movie=<Dune's id>`
- Then the response is 200 with exactly Dune's three seats in seat-number order, each with id,
  movie, seat number and booking status (A2 `true`, the others `false`)
- And `GET /api/seats/` with no filter lists every seat

**AC-11 (US-3): Book via API**
- Given I am signed in and Dune's seat A1 is available
- When a client sends `POST /api/seats/<A1's id>/book/`
- Then the response is **201** with the new booking (id, movie, seat, user, booking date)
- And A1's booking status is now `true`

**AC-12 (US-4): Sign in and out**
- Given the user "sam" exists
- When I click "Sign in" in the navbar, enter sam's username and password, and submit
- Then I return to the page I came from, and the navbar shows "sam" and a "Sign out" button
- And with a wrong password I stay on the sign-in page and see an error
- (Accounts are created by staff in the Django admin. There is no sign-up page; see Out of scope.)

**AC-13 (US-1): No seats yet**
- Given "Up" has no seats
- When I open Up's seat booking page
- Then I see "No seats for this movie yet"

**AC-14 (US-3): Bad movie filter**
- Given seats exist
- When a client sends `GET /api/seats/?movie=abc`
- Then the response is **400** with an error for `movie`, never a 500
- And `GET /api/seats/?movie=9999` (a number, but no such movie) is 200 with an empty list

## 4. Data
| Thing | Information | Rules |
|---|---|---|
| Seat | movie | **Required.** Each seat belongs to one movie (see Open questions) |
| Seat | seat number | **Required.** Text such as "A1", at most 4 characters; unique within its movie |
| Seat | booking status | Stored: `false` (available) or `true` (booked). Starts `false`; only the booking operation sets it |
| Booking | movie, seat, user, booking date | User is always the signed-in user (AC-5). Movie is always the seat's movie. Booking date is set automatically to the day it was made. At most one booking per seat, enforced by the database (AC-4); a seat already belongs to one movie, so this means one booking per seat per movie |

## 5. API / UI behavior
| Action | Input | Success result | Failure result |
|---|---|---|---|
| View seats for a movie (page) | movie id | page listing the movie's seats, each available or booked | 404 if no such movie |
| Sign in / sign out (page) | username, password | back to the previous page, signed in / signed out | sign-in page with an error |
| List seats (API) | optional `?movie=<id>` | 200, list (empty for an unknown id) | 400 if `movie` isn't a number |
| Get one seat (API) | id | 200, seat | 404 |
| Book a seat (page) | seat, signed-in user | message "Seat A1 booked for Dune" on the same page | "Seat A2 is already booked"; sign-in page if signed out; 404 if no such seat |
| Book a seat (API) | seat id, signed-in user | 201, booking | 409 taken; 403 signed out; 404 no such seat |

## 6. Out of scope
- Payments, seat maps with rows and aisles, holding a seat for 10 minutes
- Booking several seats in one request
- Creating, editing or deleting seats through the API. Seats are created in the Django admin (or
  by seed data for the Render deploy); `/api/seats/` is read-only apart from booking
- A sign-up page. Staff create accounts in the admin
- Cancelling a booking (see Open questions)

## 7. Open questions
- [x] **The assignment's Seat model has no movie field.** Is a seat booked for *every* movie, or
      is availability per movie? How do the Seat and Booking models together answer that? Decide,
      and write down why.
      → **Each seat belongs to one movie** (Seat gets a movie field). Availability is per movie,
      because Dune's A1 and Up's A1 are different seats. This keeps the assignment's
      "booking status" field meaningful, and lets the database refuse a second booking of a seat
      with a simple uniqueness rule on Booking's seat.
- [x] **One source of truth for "is this seat taken?"** Seat has a booking status, and Booking
      also records that the seat is taken. If they disagree (a booking exists but the status says
      "available"), which one is right? Decide: is the status **stored** on Seat, or **worked out**
      from bookings each time? A good answer says: (1) whether availability is global or per
      (movie, seat), (2) which data is the source of truth, (3) if you store the status, every place
      that must update it (book, cancel, admin, delete) and how you keep them in step, and (4) which
      AC and test would catch them disagreeing.
      → (1) Per (movie, seat), since each seat belongs to one movie. (2) **The Booking table is the
      source of truth**: the database's one-booking-per-seat rule is what actually prevents double
      booking. (3) Booking status is **stored** on Seat for the API and page to show, and only the
      shared booking operation sets it, in the same database transaction as creating the Booking,
      so both are saved or neither is. Cancelling is out of scope, so nothing else changes it;
      seats created in the admin start available. (4) AC-2 and AC-11 check both the new Booking and
      the status; AC-4's test saves a duplicate Booking directly and checks the status is unchanged.
- [x] **Where does "book a seat" live?** HW2 lets you book through `/api/seats/` *and*
      `/api/bookings/` (built in 003), and the page books too. All three must follow the same rules
      (AC-6 here, AC-7 in 003). Decide which one operation they all call. A good answer names the single
      place the rules (seat free? signed in? who's the user?) live, and why copying them would break AC-6.
      → **One booking operation** that takes the signed-in user and a seat, and either creates the
      booking or reports "already booked". The page, `/api/seats/<id>/book/` and 003's
      `/api/bookings/` all call it. The plan names where it lives. If each copied the rules, a fix
      in one place (say, the AC-4 race) would leave the others broken, breaking AC-6.
- [x] Can a booking be cancelled? → **No, out of scope for HW2.** It would need a second place that sets booking status back to available. Revisit only if time allows.
- [x] **`GET /api/seats/?movie=abc` returned 500** (found while building the seat list: a
      non-numeric id crashed the filter). → **400** with an error for `movie` (AC-14). An unknown
      numeric id returns 200 with an empty list.
- [x] Who creates seats? → **Staff, in the Django admin**, plus seed data for the Render deploy (planned with deployment). Without seats there's nothing to book, so the page shows "No seats for this movie yet" (AC-13).
