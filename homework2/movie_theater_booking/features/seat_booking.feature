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

  Scenario: Book an available seat
    # AC-2
    Given I am signed in as "sam"
    When I open the seat booking page for "Dune"
    And I book seat A1
    Then I see "Seat A1 booked for Dune"
    And seat A1 is shown as "Booked"
    And seat A1 for "Dune" is booked by "sam"

  Scenario: Seat already taken
    # AC-3. The page shows no Book button for A2, so this is a stale page or a
    # hand-made request posting A2 anyway.
    Given I am signed in as "sam"
    When I open the seat booking page for "Dune"
    And I try to book seat A2 anyway
    Then I see "Seat A2 is already booked"
    And seat A2 for "Dune" is booked by "someone-else"
