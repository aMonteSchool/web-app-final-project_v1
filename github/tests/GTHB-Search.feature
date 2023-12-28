Feature: GTHB - Search

  Background: Navigation
    Given Browser: navigate to Github

  @GTHB-6
  Scenario: GTHB: search for username using keyboard
    When UI: type nadvolod into Search field
    And UI: press ENTER
    Then UI: page is not empty

  @GTHB-6
  Scenario: GTHB: search for username using Search button
    When UI: type nadvolod into Search field
    And UI: "click" Search
    Then UI: page is not empty

  @GTHB-6
  Scenario Outline: GTHB: validate search for different accounts
    When UI: search for <username>
    Then UI: page <condition> empty

    Examples:
      | username               | condition |
      | nadvolod               | is not    |
      | nad volod              | is        |
      | *space*nadvolod*space* | is        |
      | *space*nadvolod        | is        |
      | nadvolod*space*        | is        |
      | *space*                | is        |
      | /                      | is        |

  @GTHB-6
  Scenario: GTHB: validate search after invalid search
    When UI: search for /
    Then UI: page is empty
    When UI: search for nadvolod
    Then UI: page is not empty