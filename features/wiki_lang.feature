Feature: Wikipedia Supports Many Languages

  Scenario: English Wikipedia Works
    Given The User is on the Wikipedia Home Page
    When The User clicks on English
    Then The User should be on the English Home Page

  Scenario: Spanish Wikipedia Works
    Given The User is on the Wikipedia Home Page
    When The User clicks on Spanish
    Then The User should be on the Spanish Home Page