Feature: The Wikipedia Search Feature Works

  Scenario Outline: Searching for various keywords
    Given The User is on the Wikipedia Home Page
    When The User types <word> in the search bar
    When The User clicks the search button
    Then The title should be <title>

  Examples:
    | word   | title              |
    | Mario  | Mario - Wikipedia  |
    | Wario  | Wario - Wikipedia  |
    | Bowser | Bowser - Wikipedia |
    | Ganon  | Ganon - Wikipedia  |