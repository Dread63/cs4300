Feature: Seat booking
  As a moviegoer, I want to see which seats are available for a movie and book one.
  (spec 002)

  Background:
    Given the movie "Dune" has seats A1, A2, A3, A4, A5
    And seat A2 for "Dune" is already booked

  Scenario: See seats for a movie
    # AC-1
    When I open the movie list page
    And I click "Book Now" for "Dune"
    Then I am on the seat booking page for "Dune"
    And seat A2 is shown as "Booked"
    And seats A1, A3, A4, A5 are shown as "Available"

  Scenario: Browse seats signed out
    # AC-8
    Given I am not signed in
    When I open the seat booking page for "Dune"
    Then seats A1, A3, A4, A5 are shown as "Available"
    And every available seat offers "Sign in to book"
