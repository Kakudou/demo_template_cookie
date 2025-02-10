Feature: Connector fails to instantiate due to invalid configuration.

  Scenario Outline: Fail to instantiate connector due to invalid configuration.
    Given an invalid 'config.yaml' file with invalid or missing value for <opencti_url>, <opencti_token>, <connector_id>, <connector_name>, <connector_scope>, <connector_log_level> , <connector_duration_period>, <connector_type>.
    When the try-to-instantiate connector attempts to parse the configuration file.
    Then an error should be logged indicating configuration issues.

    Examples:
        | opencti_url      | opencti_token | connector_id | connector_name         | connector_scope | connector_log_level | connector_duration_period | connector_type  |
        | http://fake:4242 | fake_token    | not_uuid4    | Generic Json Connector | note            | NotValid            | PT12H                     | EXTERNAL_IMPORT |
        | http://fake:4242 | fake_token    | None         | Generic Json Connector | note            | info                | None                      | EXTERNAL_IMPORT |
