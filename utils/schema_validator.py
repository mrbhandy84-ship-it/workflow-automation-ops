"""
schema_validator.py

Validates event and job payloads against registered JSON schemas.
Handles schema versioning, caching, and structured validation error output.
"""

from __future__ import annotations

from typing import Any


class SchemaValidationError(Exception):
    """Raised when a payload fails schema validation."""

    def __init__(self, errors: list[dict[str, Any]]) -> None:
        self.errors = errors
        super().__init__(f"{len(errors)} validation error(s)")


class SchemaRegistry:
    """
    Central registry for JSON schemas used across the pipeline.

    Schemas are keyed by (schema_id, version) tuples and loaded
    on first access. The registry handles resolution of $ref chains
    within loaded schemas.
    """

    def __init__(self, schema_base_path: str) -> None:
        """
        Args:
            schema_base_path: Filesystem path or URI prefix from which
                              schema files are resolved.
        """
        ...

    def register(self, schema_id: str, version: str, schema: dict[str, Any]) -> None:
        """
        Register a schema definition explicitly.

        Args:
            schema_id: Canonical schema identifier (matches $id field).
            version:   Schema version string (e.g., "1.0", "2.3").
            schema:    Parsed JSON schema dict.
        """
        ...

    def get(self, schema_id: str, version: str) -> dict[str, Any]:
        """
        Retrieve a registered schema by ID and version.

        Raises:
            KeyError: If no schema is registered for the given ID and version.
        """
        ...


class PayloadValidator:
    """
    Validates arbitrary payloads against schemas retrieved from the registry.

    Validation results are structured for downstream logging and alerting,
    not just boolean pass/fail. Error paths are reported in JSON Pointer format.
    """

    def __init__(self, registry: SchemaRegistry) -> None:
        ...

    def validate(
        self,
        payload: dict[str, Any],
        schema_id: str,
        version: str,
        strict: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Validate a payload and return structured error objects.

        Args:
            payload:   The data to validate.
            schema_id: Schema to validate against.
            version:   Schema version to use.
            strict:    If True, raise SchemaValidationError on any failure.
                       If False, return errors without raising.

        Returns:
            List of error dicts with 'path', 'message', and 'value' keys.
            Empty list on success.

        Raises:
            SchemaValidationError: If strict=True and validation fails.
        """
        ...

    def validate_event(self, event: dict[str, Any]) -> None:
        """
        Validate against the canonical event envelope schema.

        Uses the version declared in the event's 'version' field.
        Raises SchemaValidationError if the envelope or payload is invalid.
        """
        ...

    def validate_job(self, job: dict[str, Any]) -> None:
        """
        Validate against the job definition schema.

        Raises:
            SchemaValidationError: If the job definition is structurally invalid.
        """
        ...
