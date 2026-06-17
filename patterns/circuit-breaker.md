# Circuit Breaker

This pattern prevents cascading failures by tracking dependency failure rates and rejecting calls during degradation windows. Breaker state is shared across worker instances. Configuration is per-dependency, defined in the connector config.
