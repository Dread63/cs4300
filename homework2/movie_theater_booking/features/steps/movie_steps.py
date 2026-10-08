"""Steps for features/movie_listings.feature (spec 001).

behave-django runs each scenario against a fresh test database and puts a Django
test client on context.test, so these steps talk to the real views and templates.
"""
from behave import given, then, when
from bs4 import BeautifulSoup
from django.urls import reverse

from bookings.models import Movie


@given("these movies exist:")
def step_movies_exist(context):
    for row in context.table:
        Movie.objects.create(
            title=row["title"],
            description=row["description"],
            release_date=row["release_date"],
            duration=int(row["duration"]),
        )


@given("no movies exist")
def step_no_movies(context):
    # Each scenario starts with an empty test database; this makes that explicit.
    Movie.objects.all().delete()


@when("I open the movie list page")
def step_open_movie_list(context):
    context.response = context.test.client.get(reverse("movie_list"))
    context.test.assertEqual(context.response.status_code, 200)


@then('I see "{title}" with "{description}" and a "{button}" button')
def step_see_movie(context, title, description, button):
    # Check within the movie's own list item, so Dune's button can't satisfy Up's step.
    page = BeautifulSoup(context.response.content, "html.parser")
    items = [li for li in page.select("li.list-group-item") if li.h5.get_text(strip=True) == title]
    context.test.assertEqual(len(items), 1, f"expected one list item for {title!r}")
    context.test.assertIn(description, items[0].get_text())
    context.test.assertIsNotNone(items[0].find("button", string=button))


@then('I see "{text}"')
def step_see_text(context, text):
    context.test.assertContains(context.response, text)


@then("I see no movie list")
def step_no_movie_list(context):
    page = BeautifulSoup(context.response.content, "html.parser")
    context.test.assertEqual(page.select("li.list-group-item"), [])
