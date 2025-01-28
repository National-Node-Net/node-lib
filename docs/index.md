# ia-map-lib

## Actions

Actions provide automation and progress monitoring of data processing tasks. A component within Integration Architecture Node will typically be implemented using one or more of the subclasses of `Action`.

[Actions](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/actions.md) | [Adapters](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/adapters.md) | [Mappers](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/mappers.md) | [Projectors](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/projectors.md)

## Record Handling

A `DataSource` provides input from a source (e.g. a Kafka consumer), whilst a `DataSink` handles the output (e.g. a Kafka producer). 
`RecordUtils` manipulates headers.

[DataSource](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/data-sources.md) | [DataSink](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/data-sinks.md) | [RecordUtils](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/record-utils.md)


## Utilities and Helpers

ia-map-lib provides a number of features out of the box to support development, configuration, error handling and audit logging.

[Configuration](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/configuration.md) | [Logging](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/logging.md) | [Error Handling](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/error-handling.md) | [Provenance and Audit](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/provenance.md) | [Telemetry](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/telemetry.md) | [SecurityLabel modules](https://github.com/National-Digital-Twin/ia-map-lib/blob/main/docs/security-label-modules.md)
