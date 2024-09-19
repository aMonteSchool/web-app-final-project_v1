@same_browser
Feature: UHaul: Truck Rental Flow

  Background: Open home page
    Given Browser: navigate to "U-Haul"

  Scenario: Fill out the form to get Rates
    When Create a new Truck order
      | pick_up_date | 12.28.2024 |
    When Fill Out Hero form Trucks & Trailers
    Then Verify header on the page Rates


  Scenario: Select Rate -> Verify Location Page data
    When Select the truck with towing
        | towing_year  | 2018 |
        | towing_make  | BMW  |
        | towing_model | 320i |

  Scenario: Select Location
    When Select closest truck with towing
    When Skip options on page Dollies
    When Skip options on page Storage Units
    When Skip options on page Boxes & Packing
    When Skip options on page Moving Loading
    When Skip options on page Moving Unloading

  Scenario: Verify Shopping Cart
    Then Verify Shopping Cart Due at Pick Up price



