from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Movie


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
