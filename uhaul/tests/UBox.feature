@same_browser
Feature: UHaul: Rent UBox Flow

  Background: Open home page
    Given Browser: navigate to "U-Haul"

  Scenario:
    When Create a new ubox order
    And Open UBox
    And Get rates for Ranked Moving Container
        | moving_from  | 98125      |
        | loading_date | 11.21.2024 |
    And Select 2 containers and collect prices
    And Plan Ubox move
        | moving_from     | 98125                   |
        | street_address  | 14041 15th Ave NE, 204A |
        | city            | Seattle                 |
        | state           | WA                      |
    And Select delivery option
        | delivery_option | We Deliver |
    And I Skip Need Help Loading Your Items
    And I Skip Boxes & Packing Supplies
    And I Select Ubox Coverage
        | coverage | Decline storage insurance coverage |


  Scenario: Verify Shopping Cart
    Then Verify Shopping Cart for UBox order
