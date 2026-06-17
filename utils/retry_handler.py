"""
retry_handler.py

Handles retry scheduling, backoff calculation, and dead-letter escalation
for failed jobs. Decoupled from job execution — operates on job state records.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any


class BackoffStrategy(enum.Enum):
    FIXED = "fixed"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"


@dataclass
class RetryPolicy:
    """
    Defines retry behavior for a job class.

    Attributes:
        max_attempts:       Maximum number of attempts before dead-lettering.
        backoff_strategy:   Delay calculation strategy between attempts.
        backoff_base_ms:    Base delay in milliseconds.
        backoff_max_ms:     Cap on calculated delay.
        jitter:             If True, adds randomized jitter to prevent thundering herd.
        retry_on:           Set of exception class names that trigger retry.
        no_retry_on:        Set of exception class names that bypass retry entirely.
    """

    max_attempts: int
    backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL
    backoff_base_ms: int = 1000
    backoff_max_ms: int = 30000
    jitter: bool = True
    retry_on: frozenset[str] = frozenset()
    no_retry_on: frozenset[str] = frozenset()


class RetryHandler:
    """
    Determines whether a failed job should be retried and when,
    based on the applicable RetryPolicy and job state.
    """

    def __init__(self, policy_registry: dict[str, RetryPolicy]) -> None:
        """
        Args:
            policy_registry: Mapping of job_type -> RetryPolicy.
                             Falls back to 'default' policy if job_type not found.
        """
        ...

    def should_retry(
        self, job: dict[str, Any], error_class: str
    ) -> bool:
        """
        Determine whether a failed job is eligible for retry.

        Args:
            job:         Job state record including retry_count and job_type.
            error_class: Name of the exception class that caused the failure.

        Returns:
            True if the job should be rescheduled, False if it should be dead-lettered.
        """
        ...

    def next_attempt_delay_ms(self, job: dict[str, Any]) -> int:
        """
        Calculate delay before the next attempt in milliseconds.

        Applies the policy's backoff strategy and optional jitter.

        Args:
            job: Job state record with current retry_count.

        Returns:
            Delay in milliseconds. Always <= policy.backoff_max_ms.
        """
        ...

    def escalate_to_dlq(self, job: dict[str, Any], reason: str) -> dict[str, Any]:
        """
        Construct a dead-letter record from a terminal job failure.

        Args:
            job:    Job state record.
            reason: Human-readable escalation reason.

        Returns:
            Dead-letter envelope dict ready for DLQ publication.
        """
        ...
