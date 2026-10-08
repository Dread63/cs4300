"""Steps for features/booking_history.feature (spec 003).

Signing in, seats and booking come from seat_steps.py; navbar clicks from auth_steps.py.
"""
from datetime import date

from behave import then
from bs4 import BeautifulSoup
from django.urls import reverse
from django.utils.dateformat import format as format_date


@then("I am on My Bookings")
def step_on_my_bookings(context):
    context.test.assertEqual(context.response.status_code, 200)
    context.test.assertEqual(context.response.request["PATH_INFO"], reverse("booking_history"))


@then('my bookings are "{title}" seat {seat} booked today')
def step_my_bookings_are(context, title, seat):
    page = BeautifulSoup(context.response.content, "html.parser")
    rows = [[td.get_text(strip=True) for td in tr.find_all("td")] for tr in page.select("tr[data-booking]")]
    context.test.assertEqual(rows, [[title, seat, format_date(date.today(), "M j, Y")]])
