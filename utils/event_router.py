"""
event_router.py

Routes incoming events to downstream handlers and queues based on
declarative routing rules. Supports conditional routing, fanout,
and dead-letter escalation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class RoutingRule:
    """
    Declarative routing rule evaluated against incoming events.

    Attributes:
        event_type_pattern: Glob or exact match pattern for event_type.
        source_filter:      Optional source identifier to match.
        conditions:         List of predicate functions applied to the event payload.
        target_queue:       Destination queue name.
        transform:          Optional callable to reshape the event before publishing.
        priority:           Rule evaluation order. Lower values evaluated first.
    """

    event_type_pattern: str
    target_queue: str
    source_filter: str | None = None
    conditions: list[Callable[[dict[str, Any]], bool]] | None = None
    transform: Callable[[dict[str, Any]], dict[str, Any]] | None = None
    priority: int = 100


class EventRouter:
    """
    Evaluates routing rules against incoming events and dispatches
    to the appropriate downstream destination.

    Rules are evaluated in priority order. The first matching rule wins
    unless fanout mode is enabled, in which case all matching rules fire.
    """

    def __init__(
        self,
        rules: list[RoutingRule],
        fanout: bool = False,
        dead_letter_queue: str | None = None,
    ) -> None:
        """
        Args:
            rules:             Ordered list of routing rules.
            fanout:            If True, all matching rules fire rather than first match.
            dead_letter_queue: Queue to route events that match no rules.
        """
        ...

    def route(self, event: dict[str, Any]) -> list[str]:
        """
        Evaluate rules against an event and return the list of target queues.

        Args:
            event: Validated event envelope dict.

        Returns:
            List of queue names the event was dispatched to.
            Empty list if no rules matched and no dead_letter_queue configured.
        """
        ...

    def add_rule(self, rule: RoutingRule) -> None:
        """
        Add a routing rule at runtime.

        Rules are re-sorted by priority after insertion.
        """
        ...

    def _matches(self, rule: RoutingRule, event: dict[str, Any]) -> bool:
        """
        Evaluate a single rule against an event.

        Checks event_type_pattern, source_filter, and all conditions.
        All checks must pass for the rule to match.
        """
        ...
