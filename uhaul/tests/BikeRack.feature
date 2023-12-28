@same_browser
Feature: UHaul: Bike Rack Buy Flow

  Background: Open home page
    Given Browser: navigate to "U-Haul"

  Scenario: Select Bike Racks
    When Create a new Bike Racks order
    When Select from Hitches & Accessories menu Bike Rack option
    When Verify header on the page Bike Racks
    When Set filter on page Bike Racks
      | No. of Bikes| 2|
#      | Brand       |  |
#      | Rack Type   |  |
#      | Features    |  |
    And Verify Results number
    When Select 2 random Bike Rack item
    Then Verify Shopping Cart Due at Subtotal price