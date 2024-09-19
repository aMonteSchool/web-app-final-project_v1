@same_browser
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

  Scenario: Select Rate
    When Select storage
      | storage_name | U-Haul Moving & Storage of Greater Miami |
    And Select unit
      | storage_type | 5' x 8' x 8' |
    And Select insurance
      | insurance_type | Use my homeowners/renters insurance |

  Scenario: Verify Shopping Cart
    Then Verify Shopping Cart Self-Storage Rental