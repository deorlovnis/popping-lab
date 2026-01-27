# Hypothesis: Phoenix Traces Instrument and Prompt Spans

**Claim:** When `run_experiment` executes an agent with tools, Phoenix records
distinct spans for: (1) the agent session, and (2) each tool call.

**Falsification criteria:**
- Zero spans found for the experiment's trace ID → FALSIFIED
- No span named `agent-session` → FALSIFIED
- No span named `tool:calculate` → FALSIFIED

**Why it matters:** If tracing doesn't capture instrument and prompt activity,
the lab has no observability into experiment runs.
