# Saga Pattern

The saga pattern manages distributed transactions across multiple services without relying on two-phase commit. Each step in the workflow executes a local transaction and publishes an event or message to trigger the next step. If any step fails, the saga executes compensating transactions in reverse order to undo the changes from completed steps.

There are two implementation variants: choreography-based sagas, where each service listens for events and decides autonomously what to do next, and orchestration-based sagas, where a central coordinator issues commands to each participant and tracks overall state. Choreography is simpler to deploy but difficult to observe and reason about as the number of participants grows. Orchestration adds a coordination point but makes the overall state machine explicit and auditable.

In practice, the orchestration variant is more maintainable for workflows with more than three to four steps. The key operational investment is in compensation logic — compensating transactions are not rollbacks in the database sense. They are forward-moving operations that return the system to a consistent state, and they must themselves be idempotent and retry-safe. Compensation that fails is a production incident, not a configuration problem.

State persistence for the saga coordinator is non-negotiable. The coordinator must survive process restarts and be able to resume from the last known step. Event sourcing is a natural fit here: the saga's history is the state, and replaying events reconstructs the current position without external checkpointing.
