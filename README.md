# workflow-automation-ops

Reference architecture for production workflow automation systems. This repository captures structural patterns, schema conventions, and operational configurations used across event-driven and scheduled automation pipelines.

This is not a starter kit. The contents here reflect decisions already made in deployed systems — what survived contact with production, what got replaced, and why. Schemas define contract boundaries. Configs show structural intent without environment-specific values. Patterns document tradeoffs, not procedures.

## Repository Layout

```
schemas/       — canonical event and job schemas, versioned by surface
configs/       — orchestration and queue configurations (placeholder values)
patterns/      — practitioner notes on structural patterns in use
utils/         — Python stubs for shared operational utilities
docs/          — architecture context and decision records
```

## Design Principles

- **Schema-first**: Contract boundaries are defined in schemas before any pipeline is wired. Downstream consumers declare what they need; producers adapt.
- **Idempotency by default**: Every job is designed to be replayed safely. Side effects are tracked at the job level, not assumed to be guarded upstream.
- **Explicit failure paths**: Retry policy, dead-letter routing, and timeout behavior are configured per job class — not inherited from platform defaults.
- **Separation of concerns**: Trigger logic, execution logic, and state management are distinct layers. Mixing them is the primary source of operational debt in automation systems.

## Status

Active reference. Schemas and configs are updated when production systems diverge meaningfully from what's documented here. Not all patterns in `/patterns` are currently in use — some are retained because they describe what was tried and why it was set aside.

---

Part of the HOA systems stack — handsonanalytics.net
