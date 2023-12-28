Feature: GTHB - Fields

  Background: Navigation
    Given Browser: navigate to Github

  @GTHB-5 @GTHB-25 @GTHB-32 @GTHB-39
  Scenario Outline: GTHB Integration API: verify summary info
    When UI: search for <username>
    And API: send GET request to users/<username>
    And API: verify status code is 200
    Then GitHub Integration API: Summary: verify param values
      | label     |
      | Repos     |
      | Followers |
      | Following |
      | Gists     |

    Examples: data exists
      | username |
      | nadvolod |

    Examples: no data
      | username   |
      | mfedemiria |
