Feature: Booking history
  As a moviegoer, I want to see a list of my bookings, so that I know what I've reserved.
  (spec 003)

  Scenario: See my bookings
    # AC-1: book on the seat page, then find it in My Bookings
    Given the movie "Dune" has seats A1, A2
    And I am signed in as "sam"
    When I open the seat booking page for "Dune"
    And I book seat A1
    And I click "My Bookings" in the navbar
    Then I am on My Bookings
    And my bookings are "Dune" seat A1 booked today

  Scenario: No bookings yet
    # AC-5
    Given I am signed in as "pat"
    When I open the movie list page
    And I click "My Bookings" in the navbar
    Then I am on My Bookings
    And I see "You haven't booked any seats yet"
