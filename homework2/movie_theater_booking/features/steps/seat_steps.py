"""Steps for features/seat_booking.feature (spec 002).

Steps from movie_steps.py (such as "I open the movie list page") are shared: Behave loads
every file in steps/.
"""
from datetime import date

from behave import given, then, when
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.urls import reverse

from bookings.models import Movie, Seat


def seat_numbers(text):
    """'A1, A3, A4' -> ['A1', 'A3', 'A4']"""
    return [n.strip() for n in text.split(",")]


def seat_rows(context):
    """Map each seat number on the current page to its row element."""
    page = BeautifulSoup(context.response.content, "html.parser")
    return {li["data-seat"]: li for li in page.select("li[data-seat]")}


@given('the movie "{title}" has seats {seats}')
def step_movie_with_seats(context, title, seats):
    movie = Movie.objects.create(title=title, release_date=date(2021, 10, 22), duration=155)
    for n in seat_numbers(seats):
        Seat.objects.create(movie=movie, seat_number=n)


@given('seat {seat} for "{title}" is already booked')
def step_seat_booked(context, seat, title):
    someone = User.objects.create_user("someone-else", password="pw-other-123")
    Seat.objects.get(movie__title=title, seat_number=seat).book(someone)


@given("I am not signed in")
def step_signed_out(context):
    context.test.client.logout()


@when('I click "{link}" for "{title}"')
def step_click_for_movie(context, link, title):
    page = BeautifulSoup(context.response.content, "html.parser")
    item = next(li for li in page.select("li.list-group-item") if li.h5.get_text(strip=True) == title)
    context.response = context.test.client.get(item.find("a", string=link)["href"])


@when('I open the seat booking page for "{title}"')
def step_open_seat_page(context, title):
    movie = Movie.objects.get(title=title)
    context.response = context.test.client.get(reverse("book_seat", args=[movie.id]))


@then('I am on the seat booking page for "{title}"')
def step_on_seat_page(context, title):
    movie = Movie.objects.get(title=title)
    context.test.assertEqual(context.response.status_code, 200)
    context.test.assertEqual(context.response.request["PATH_INFO"], reverse("book_seat", args=[movie.id]))
    context.test.assertContains(context.response, title)


@then('seat {seat} is shown as "{status}"')
def step_seat_shown_as(context, seat, status):
    context.test.assertIn(status, seat_rows(context)[seat].get_text())


@then('seats {seats} are shown as "{status}"')
def step_seats_shown_as(context, seats, status):
    rows = seat_rows(context)
    for n in seat_numbers(seats):
        context.test.assertIn(status, rows[n].get_text(), f"seat {n}")


@then('every available seat offers "{link}"')
def step_available_seats_offer(context, link):
    available = [li for li in seat_rows(context).values() if "Available" in li.get_text()]
    context.test.assertTrue(available)
    for li in available:
        context.test.assertIsNotNone(li.find("a", string=link), li["data-seat"])
