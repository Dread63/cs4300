Feature: Movie listings
  As a moviegoer, I want to see a list of movies, so that I can pick one to watch.
  (spec 001)

  Scenario: Browse the movie list
    # AC-1
    Given these movies exist:
      | title | description            | release_date | duration |
      | Dune  | Spice.                 | 2021-10-22   | 155      |
      | Up    | A house with balloons. | 2009-05-29   | 96       |
    When I open the movie list page
    Then I see "Dune" with "Spice." and a "Book Now" button
    And I see "Up" with "A house with balloons." and a "Book Now" button
