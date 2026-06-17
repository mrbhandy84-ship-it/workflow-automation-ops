# Fan-Out / Fan-In

The fan-out/fan-in pattern addresses workflows where a single input must spawn multiple parallel execution branches that eventually converge on an aggregated result. The canonical use case is batch processing: one trigger event produces N child jobs, each handling a subset of the work, with a terminal aggregation step blocked until all children reach a terminal state.

The primary operational challenge is tracking completion across distributed, asynchronous branches. Naive implementations poll for job status or rely on shared counters, both of which introduce race conditions under retry pressure. The more durable approach is event-based completion signaling — each child emits a typed completion event, and the aggregation step maintains a counter in a state store with compare-and-swap semantics. Only when the counter reaches N does the aggregation job become eligible for execution.

A second consideration is partial failure handling. Strict fan-in — where all branches must succeed — is rarely the right default. Most production workflows benefit from configuring a minimum success threshold (e.g., 80% of branches) beyond which the aggregation step proceeds with available results and flags partial completion. This keeps the workflow recoverable without requiring manual intervention on transient branch failures.

Child job isolation is also important: each branch must carry the parent workflow ID and branch index in its job definition. Without this, correlation during aggregation requires cross-referencing job metadata that may not be consistent across retries.
