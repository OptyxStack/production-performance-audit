# Load Testing with k6

Load tests validate hypotheses, not ego.

---

## What to test

- One critical user journey
- One bottleneck hypothesis
- One saturation point

Avoid testing everything at once.

---

## Metrics to watch

- P95 / P99 latency
- Error rate
- Resource utilization
- Queue depth

---

## Load patterns

- Ramp-up
- Sustained peak
- Spike

Production rarely sees constant load.

---

## Interpreting results

- Latency increases before errors
- Flat CPU ≠ healthy system
- Retries amplify load

---

## Common mistakes

- Testing from localhost
- Ignoring warm-up
- Comparing to averages
