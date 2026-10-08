from datetime import date

from django.contrib.auth.models import User

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Booking, Movie, Seat, SeatAlreadyBooked


class MovieModelTests(TestCase):
    """Data rules for Movie (spec 001 §4, AC-10)."""

    def test_movie_str_and_ordering(self):
        up = Movie.objects.create(
            title="Up", release_date=date(2009, 5, 29), duration=96
        )
        dune = Movie.objects.create(
            title="Dune", description="", release_date=date(2021, 10, 22), duration=155
        )

        self.assertEqual(str(dune), "Dune")
        # AC-10: newest release first, by default, for every query.
        self.assertEqual(list(Movie.objects.all()), [dune, up])
        # §4: description is optional, so a blank one passes validation.
        dune.full_clean()


class MovieAPITests(APITestCase):
    """The /api/movies/ endpoints (spec 001 AC-4 to AC-8)."""

    def setUp(self):
        self.dune = Movie.objects.create(
            title="Dune",
            description="Spice.",
            release_date=date(2021, 10, 22),
            duration=155,
        )
        self.up = Movie.objects.create(
            title="Up", release_date=date(2009, 5, 29), duration=96
        )

    def test_list_movies(self):
        response = self.client.get("/api/movies/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(
            response.json()[0],
            {
                "id": self.dune.id,
                "title": "Dune",
                "description": "Spice.",
                "release_date": "2021-10-22",
                "duration": 155,
            },
        )

    def test_create_movie(self):
        data = {
            "title": "Arrival",
            "description": "Linguists meet aliens.",
            "release_date": "2016-11-11",
            "duration": 116,
        }

        response = self.client.post("/api/movies/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        titles = [m["title"] for m in self.client.get("/api/movies/").json()]
        self.assertIn("Arrival", titles)

    def test_create_movie_missing_title_400(self):
        data = {"release_date": "2016-11-11", "duration": 116}

        response = self.client.post("/api/movies/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.json())
        self.assertEqual(Movie.objects.count(), 2)  # nothing saved

    def test_create_movie_missing_release_date_400(self):
        data = {"title": "Arrival", "duration": 116}

        response = self.client.post("/api/movies/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("release_date", response.json())
        self.assertEqual(Movie.objects.count(), 2)  # nothing saved

    def test_create_movie_zero_duration_400(self):
        # Boundary: 0 is the edge case, -5 is the "less than 0" equivalence class.
        for duration in (0, -5):
            with self.subTest(duration=duration):
                data = {"title": "Arrival", "release_date": "2016-11-11", "duration": duration}

                response = self.client.post("/api/movies/", data, format="json")

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn("duration", response.json())
                self.assertEqual(Movie.objects.count(), 2)  # nothing saved

    def test_retrieve_movie(self):
        response = self.client.get(f"/api/movies/{self.dune.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.dune.id,
                "title": "Dune",
                "description": "Spice.",
                "release_date": "2021-10-22",
                "duration": 155,
            },
        )

    def test_get_missing_movie_404(self):
        response = self.client.get("/api/movies/9999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_movie(self):
        url = f"/api/movies/{self.dune.id}/"

        # PUT replaces the whole movie, so every required field is sent.
        response = self.client.put(
            url,
            {"title": "Dune: Part One", "release_date": "2021-10-22", "duration": 156},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], "Dune: Part One")
        self.assertEqual(response.json()["duration"], 156)

        # PATCH changes only the fields sent.
        response = self.client.patch(url, {"duration": 155}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["duration"], 155)
        self.assertEqual(response.json()["title"], "Dune: Part One")

        self.dune.refresh_from_db()
        self.assertEqual((self.dune.title, self.dune.duration), ("Dune: Part One", 155))

    def test_delete_movie(self):
        url = f"/api/movies/{self.dune.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movie.objects.filter(id=self.dune.id).exists())
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)


class MovieListPageTests(TestCase):
    """The movie list page at / (spec 001 AC-1 to AC-3, AC-9)."""

    def setUp(self):
        Movie.objects.create(
            title="Dune",
            description="Spice.",
            release_date=date(2021, 10, 22),
            duration=155,
        )

    def test_movie_list_uses_base_template(self):
        response = self.client.get(reverse("movie_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/movie_list.html")
        self.assertTemplateUsed(response, "bookings/base.html")
        self.assertContains(response, "bootstrap.min.css")
        self.assertContains(response, f'href="{reverse("movie_list")}">Movies</a>', html=False)

    def test_movie_list_shows_release_date_and_duration(self):
        response = self.client.get(reverse("movie_list"))

        self.assertContains(response, "Oct 22, 2021")
        self.assertContains(response, "155 min")

    def test_movie_list_empty_state(self):
        Movie.objects.all().delete()

        response = self.client.get(reverse("movie_list"))

        self.assertContains(response, "No movies are showing right now")
        self.assertNotContains(response, "list-group-item")


class SeatModelTests(TestCase):
    """Data rules for Seat (spec 002 §4, AC-10)."""

    def setUp(self):
        self.dune = Movie.objects.create(
            title="Dune", release_date=date(2021, 10, 22), duration=155
        )
        self.up = Movie.objects.create(
            title="Up", release_date=date(2009, 5, 29), duration=96
        )

    def test_seat_str_ordering_and_unique_number_per_movie(self):
        a2 = Seat.objects.create(movie=self.dune, seat_number="A2")
        a1 = Seat.objects.create(movie=self.dune, seat_number="A1")

        self.assertEqual(str(a1), "Dune A1")
        self.assertFalse(a1.booking_status)  # new seats start available
        self.assertEqual(list(self.dune.seats.all()), [a1, a2])
        # The same number is fine for another movie: seats belong to one movie.
        Seat.objects.create(movie=self.up, seat_number="A1")
        # But not twice for the same movie; the database refuses it.
        with self.assertRaises(IntegrityError):
            Seat.objects.create(movie=self.dune, seat_number="A1")


class BookingModelTests(TestCase):
    """Data rules for Booking (spec 002 §4, AC-4)."""

    def setUp(self):
        self.sam = User.objects.create_user("sam", password="pw-sam-123")
        self.alex = User.objects.create_user("alex", password="pw-alex-123")
        self.dune = Movie.objects.create(
            title="Dune", release_date=date(2021, 10, 22), duration=155
        )
        self.a1 = Seat.objects.create(movie=self.dune, seat_number="A1")

    def test_duplicate_booking_rejected_by_database(self):
        booking = Booking.objects.create(movie=self.dune, seat=self.a1, user=self.sam)

        self.assertEqual(booking.booking_date, date.today())  # set automatically
        self.assertEqual(str(booking), "sam: Dune A1")
        # AC-4: even code that skips every check can't save a second booking of A1.
        with self.assertRaises(IntegrityError):
            Booking.objects.create(movie=self.dune, seat=self.a1, user=self.alex)

    def test_seat_book_creates_booking_and_sets_status(self):
        booking = self.a1.book(self.sam)

        # AC-2: one booking, for me, for the seat's movie, dated today.
        self.assertEqual(
            (booking.user, booking.movie, booking.seat, booking.booking_date),
            (self.sam, self.dune, self.a1, date.today()),
        )
        self.assertEqual(Booking.objects.count(), 1)
        self.a1.refresh_from_db()
        self.assertTrue(self.a1.booking_status)

    def test_seat_book_taken_raises(self):
        original = self.a1.book(self.sam)
        # A fresh copy, as a second request would load it from the database.
        a1_again = Seat.objects.get(pk=self.a1.pk)

        with self.assertRaisesMessage(SeatAlreadyBooked, "Seat A1 is already booked"):
            a1_again.book(self.alex)

        # AC-3: nothing changes; A1 still has exactly one booking, the original one.
        self.assertEqual(list(Booking.objects.all()), [original])

    def test_seat_book_race_raises_already_booked(self):
        # Another request won the race: its booking exists, but this request already
        # read A1 as available. Simulate that by saving a booking without the status.
        winner = Booking.objects.create(movie=self.dune, seat=self.a1, user=self.sam)

        with self.assertRaisesMessage(SeatAlreadyBooked, "Seat A1 is already booked"):
            self.a1.book(self.alex)

        # AC-4: still exactly one booking, and the losing request changed nothing.
        self.assertEqual(list(Booking.objects.all()), [winner])
        self.a1.refresh_from_db()
        self.assertFalse(self.a1.booking_status)


class SeatAPITests(APITestCase):
    """The /api/seats/ endpoints (spec 002 AC-3 to AC-11)."""

    def setUp(self):
        self.sam = User.objects.create_user("sam", password="pw-sam-123")
        self.dune = Movie.objects.create(
            title="Dune", release_date=date(2021, 10, 22), duration=155
        )
        self.up = Movie.objects.create(
            title="Up", release_date=date(2009, 5, 29), duration=96
        )
        self.a1, self.a2, self.a3 = (
            Seat.objects.create(movie=self.dune, seat_number=n) for n in ("A1", "A2", "A3")
        )
        self.a2.book(self.sam)
        self.up_a1 = Seat.objects.create(movie=self.up, seat_number="A1")

    def test_list_seats_filtered_by_movie(self):
        response = self.client.get("/api/seats/", {"movie": self.dune.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [
                {"id": self.a1.id, "movie": self.dune.id, "seat_number": "A1", "booking_status": False},
                {"id": self.a2.id, "movie": self.dune.id, "seat_number": "A2", "booking_status": True},
                {"id": self.a3.id, "movie": self.dune.id, "seat_number": "A3", "booking_status": False},
            ],
        )

    def test_list_all_seats(self):
        response = self.client.get("/api/seats/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)

    def test_list_seats_bad_movie_filter_400(self):
        response = self.client.get("/api/seats/", {"movie": "abc"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("movie", response.json())
        # A number with no such movie isn't an error, just no seats.
        response = self.client.get("/api/seats/", {"movie": 9999})
        self.assertEqual((response.status_code, response.json()), (200, []))

    def test_book_seat_via_api_201(self):
        self.client.force_authenticate(self.sam)

        response = self.client.post(f"/api/seats/{self.a1.id}/book/")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.get(seat=self.a1)
        self.assertEqual(
            response.json(),
            {
                "id": booking.id,
                "movie": self.dune.id,
                "seat": self.a1.id,
                "user": self.sam.id,
                "booking_date": date.today().isoformat(),
            },
        )
        self.a1.refresh_from_db()
        self.assertTrue(self.a1.booking_status)

    def test_book_taken_seat_via_api_409(self):
        self.client.force_authenticate(self.sam)

        response = self.client.post(f"/api/seats/{self.a2.id}/book/")

        # AC-3: A2 was booked in setUp; refused with 409 and the same message as the page.
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.json(), {"detail": "Seat A2 is already booked"})
        self.assertEqual(Booking.objects.filter(seat=self.a2).count(), 1)

    def test_duplicate_booking_returns_error_not_500(self):
        # AC-4: another request won the race; A1's booking exists but its status still
        # says available, so the check passes and the database refuses the save.
        Booking.objects.create(movie=self.dune, seat=self.a1, user=self.sam)
        self.client.force_authenticate(self.sam)

        response = self.client.post(f"/api/seats/{self.a1.id}/book/")

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.json(), {"detail": "Seat A1 is already booked"})

    def test_book_via_api_signed_out_403(self):
        response = self.client.post(f"/api/seats/{self.a1.id}/book/")

        # AC-8: 403 (not 401: DRF's session auth sends no WWW-Authenticate header).
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Booking.objects.filter(seat=self.a1).exists())

    def test_missing_seat_api_404(self):
        self.client.force_authenticate(self.sam)

        # AC-9: no seat 9999, whether you look it up or try to book it.
        self.assertEqual(self.client.get("/api/seats/9999/").status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            self.client.post("/api/seats/9999/book/").status_code, status.HTTP_404_NOT_FOUND
        )
        self.assertEqual(Booking.objects.count(), 1)  # only setUp's A2
