@same_browser
Feature: UHaul: Truck Rental Flow

  Background: Open home page
    Given Browser: navigate to "U-Haul"

  Scenario: Fill out the form to get Rates
    When Create a new Truck order
      | pick_up_date | 01.13.2024 |
    When Fill Out Hero form Trucks & Trailers
    Then Verify header on the page Rates


  Scenario: Select Rate -> Verify Location Page data
    When Select the truck rate
    When Verify price on Select a Location page
    When Verify size on Select a Location page

  Scenario: Select Location
    When Select closest truck
    When Add options on page Dollies
      | Utility Dolly  | 2         |
      | Furniture Pads | 3 dozen |
    When Skip options on page Storage Units
    When Skip options on page Boxes & Packing
    When Skip options on page Moving Loading
    When Skip options on page Moving Unloading
    Then Verify Shopping Cart Due at Pick Up price



