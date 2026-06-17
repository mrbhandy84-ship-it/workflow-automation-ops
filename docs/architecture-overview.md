# Architecture Overview

## System Boundaries

This stack operates as an internal automation layer — it is not a product surface. Upstream systems submit events or jobs through defined contract boundaries (schemas in `/schemas`). Downstream systems receive completion events or side effects. The orchestrator does not own business logic; it owns execution coordination and operational reliability.

## Execution Model

The primary execution model is queue-backed, worker-pull. Jobs are submitted to prioritized queues and consumed by stateless workers. Workers do not maintain workflow state; all state lives in the state store. This means workers can be scaled, restarted, or replaced without affecting in-progress workflows beyond the visibility timeout window.

Scheduled workflows are managed by a separate trigger layer. Scheduled triggers emit standard events into the event bus, which are then processed identically to external events. There is no scheduler-specific execution path.

## State Management

Workflow state is checkpointed at each step boundary. Workers write a checkpoint record before acknowledging a step completion event. If a worker dies mid-step, the step re-executes on timeout — this is acceptable because all step handlers are required to be idempotent. Steps that cannot be made idempotent are wrapped in deduplication guards keyed on the job's `idempotency_key`.

## Observability Model

All workflow events, job state transitions, and retry actions produce structured log entries with `workflow_id`, `job_id`, `tenant_id`, and `correlation_id`. These four fields are the primary axes for operational queries. Traces are emitted for every job execution, correlated by `correlation_id`. Dashboards are built on top of the metrics exporter, not log queries — log queries are for incident investigation, not routine monitoring.

## Operational Boundaries

Teams consuming this stack own their workflow definitions and retry policies. The platform owns queue infrastructure, schema registry, and state store. Issues at the workflow level (bad logic, wrong retry policy) are consuming team problems. Issues at the platform level (queue unavailability, state store lag) are platform problems. The DLQ is the primary escalation surface between the two.
