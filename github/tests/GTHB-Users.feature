Feature: GTHB - Users

  Background: Navigation
    Given Browser: navigate to Github

  @GTHB-53 @GTHB-60 @GTHB-95 @GTHB-67 @GTHB-74 @GTHB-81 @GTHB-88
  Scenario: GTHB Integration API: data exists - verify user info
    When UI: search for nadvolod
    And API: send GET request to github/users/nadvolod
    And API: verify status code is 200
    Then GitHub Integration API: User: verify param values
      | label    |
      | name     |
      | twitter  |
      | bio      |
      | company  |
      | location |
      | blog     |

  @GTHB-53 @GTHB-60 @GTHB-95 @GTHB-67 @GTHB-74 @GTHB-81 @GTHB-88
  Scenario Outline: GTHB Integration API: empty data - verify user info
    When UI: search for mfedemiria
    And API: send GET request to github/users/mfedemiria
    And API: verify status code is 200
    Then GitHub Integration API: User: verify param values
      | label   |
      | <label> |

    Examples: data exists
      | label    |
      | name     |
      | twitter  |
      | bio      |
      | company  |
      | location |
      | blog     |


  @GTHB-7 @GTHB-88 @GTHB-81
  Scenario Outline: GTHB Integration API: verify navigation links
    When UI: search for <username>
    And API: send GET request to github/<endpoint>
    And API: verify status code is 200
    Then GitHub Integration API: verify navigation link for <field>

    Examples:
      | field     | username | endpoint                              |
      | Blog      | nadvolod | users/nadvolod                        |
      | Follow    | nadvolod | users/nadvolod                        |
      | Followers | nadvolod | users/nadvolod/followers?per_page=100 |