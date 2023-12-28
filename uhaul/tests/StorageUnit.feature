Feature: UHaul: Storage Rental Flow

  Background: Open home page
    Given Browser: navigate to "U-Haul"


  Scenario: Get rates for Storage
    When Create a new Storage order
    When Fill Out Hero form Storage Units
    Then Validate Filter & Sort Locations checked boxes
      | Unit Size | Small          |
      | Unit Size | Medium         |
      | Features  | Indoor Storage |