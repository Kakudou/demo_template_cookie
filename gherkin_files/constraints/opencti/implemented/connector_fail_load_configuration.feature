Feature: Fail to load configuration due to missing file.

  Scenario: Fail to load configuration due to missing file.
    Given the 'config.yaml' file does not exist.
    When the try-to-instantiate connector attempts to parse the configuration file.
    Then an error should be logged indicating a failure to load the configuration file.
