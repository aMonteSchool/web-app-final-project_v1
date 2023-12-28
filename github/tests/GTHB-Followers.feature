Feature: GTHB - Followers

  Background: Navigation
    Given Browser: navigate to Github

  @GTHB-7
  Scenario Outline: GTHB Integration API: verify followers info
    When UI: search for <username>
    And API: send GET request to users/<username>/followers?per_page=100
    And API: verify status code is 200
    Then GitHub Integration API: Followers: verify param values
      | label     |
      | Usernames |
      | Links     |

    Examples: data exists
      | username |
      | nadvolod |

    Examples: no data
      | username   |
      | mfedemiria |


  @GTHB-7
  Scenario Outline: GTHB Integration API: verify number of followers
    When UI: search for <username>
    And API: send GET request to users/<username>/followers?per_page=100
    And API: verify status code is 200
    Then GitHub Integration API: Followers: verify total amount

    Examples: data exists
      | username |
      | nadvolod |

    Examples: partial data
      | username |
      | fedynich |

    Examples: no data
      | username   |
      | mfedemiria |