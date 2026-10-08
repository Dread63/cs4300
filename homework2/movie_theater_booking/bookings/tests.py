from datetime import date

from django.test import TestCase
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
