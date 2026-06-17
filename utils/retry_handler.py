import enum


class BackoffStrategy(enum.Enum):
    FIXED = "fixed"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"


class RetryPolicy:
    def __init__(self, max_attempts, backoff_strategy, backoff_base_ms,
                 backoff_max_ms, jitter, retry_on, no_retry_on):
        pass


class RetryHandler:
    def __init__(self, policy_registry):
        pass

    def should_retry(self, job, error_class):
        raise NotImplementedError

    def next_attempt_delay_ms(self, job):
        raise NotImplementedError

    def escalate_to_dlq(self, job, reason):
        raise NotImplementedError
