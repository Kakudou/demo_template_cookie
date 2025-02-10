Feature: Load OpenCTI connector configuration and instantiate the connector.

  Scenario Outline: Successfully load configuration and instantiate the OpenCTI connector.
    Given a valid 'config.yaml' file exists, with <opencti_url>, <opencti_token>, <connector_id>, <connector_name>, <connector_scope>, <connector_log_level> , <connector_duration_period>, <connector_type>.
    When i instantiate the OpenCTI connector.
    Then the OpenCTI connector should be instantiated.
    And the connector should be initialized with the correct settings.

    Examples:
        | opencti_url      | opencti_token | connector_id                         | connector_name     | connector_scope | connector_log_level | connector_duration_period | connector_type |
        | http://fake:4242 | fake_token    | aba9b448-5d03-43e3-bfdd-fd24bf9a2c5c | DemoTemp | note            | info                | PT12H                     | EXTERNAL_IMPORT |
