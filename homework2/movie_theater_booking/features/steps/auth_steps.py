"""Steps for features/sign_in.feature (spec 002 AC-12)."""
from behave import given, then, when
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.urls import reverse


def navbar(context):
    return BeautifulSoup(context.response.content, "html.parser").select_one("nav")


@given('the user "{username}" exists with password "{password}"')
def step_user_exists(context, username, password):
    User.objects.create_user(username, password=password)


@when('I click "{link}" in the navbar')
def step_click_navbar(context, link):
    href = navbar(context).find("a", string=link)["href"]
    context.response = context.test.client.get(href)


@when('I sign in as "{username}" with password "{password}"')
def step_sign_in(context, username, password):
    # Fill in the sign-in form on the page, keeping its hidden "next" field.
    form = BeautifulSoup(context.response.content, "html.parser").select_one("main form")
    data = {"next": form.select_one('[name="next"]')["value"], "username": username, "password": password}
    context.response = context.test.client.post(reverse("login"), data, follow=True)


@when("I sign out")
def step_sign_out(context):
    context.response = context.test.client.post(reverse("logout"), follow=True)


@then('the navbar shows "{first}" and "{second}"')
def step_navbar_shows_both(context, first, second):
    text = navbar(context).get_text(" ", strip=True)
    context.test.assertIn(first, text)
    context.test.assertIn(second, text)


@then('the navbar shows "{text}"')
def step_navbar_shows(context, text):
    context.test.assertIn(text, navbar(context).get_text(" ", strip=True))


@then("I am on the sign-in page")
def step_on_sign_in_page(context):
    context.test.assertEqual(context.response.request["PATH_INFO"], reverse("login"))
    context.test.assertTemplateUsed(context.response, "registration/login.html")
