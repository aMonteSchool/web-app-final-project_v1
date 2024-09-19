@same_browser
Feature: UHaul: Rent Bike Rack Flow

  Background: Open home page
    Given Browser: navigate to "U-Haul"

  Scenario: Select Bike Rack
    When Create a new bike racks order
    When I open Hitches & Accessories
    And I open Shop Bike Racks

  Scenario: Order Bike Rack
    When I select Bike Rack
      | bike_rack | Swagman XC 2 Bike Rack |
    And I select Ship to me delivery
    And I click Add to Cart
    And I click View Cart

  Scenario: Verify Shopping Cart
    Then Verify Shopping Cart for Bike Rack


