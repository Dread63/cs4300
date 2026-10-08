Feature: Sign in
  As a moviegoer, I want to sign in, so that my bookings are mine.
  (spec 002 US-4)

  Background:
    Given the user "sam" exists with password "pw-sam-123"
    And the movie "Dune" has seats A1, A2

  Scenario: Sign in and come back
    # AC-12
    When I open the seat booking page for "Dune"
    And I click "Sign in" in the navbar
    And I sign in as "sam" with password "pw-sam-123"
    Then I am on the seat booking page for "Dune"
    And the navbar shows "sam" and "Sign out"
    When I sign out
    Then the navbar shows "Sign in"

  Scenario: Wrong password
    # AC-12
    When I open the movie list page
    And I click "Sign in" in the navbar
    And I sign in as "sam" with password "wrong"
    Then I am on the sign-in page
    And I see "Please enter a correct username and password"
