# Production Performance Audit Playbook

This playbook is a **systematic, evidence-first approach** to identify what actually limits a production system today.

It is designed for:
- CTOs / Tech Leads
- Founders of growing products
- Senior engineers responsible for uptime and cost

---

## What a performance audit is (and is not)

A real performance audit is **not**:
- Checking CPU / memory once
- Running Lighthouse on homepage
- Guessing based on intuition

A real audit answers one question clearly:

> What constraint is currently limiting this system, and what decision should we make next?

---

## Step 1 — Define the business-level symptom

Start with observable pain:
- Slow checkout
- Latency spikes during campaigns
- High infra cost without traffic growth
- Random timeouts under load

Document:
- When does it happen?
- Which user flows are affected?
- What is the business impact?

---

## Step 2 — Establish a baseline (before touching anything)

You must capture **before** data.

Minimum baseline:
- P50 / P95 / P99 latency
- Error rate
- Throughput (RPS / QPS)
- CPU, memory, IO
- Database query latency
- Cache hit ratio

Without this, improvements cannot be proven.

---

## Step 3 — Map the request path

For a single critical request:
Client → CDN → Load Balancer → App → Cache → DB → External APIs

For each hop, ask:
- Is latency increasing?
- Is contention present?
- Is concurrency bounded?

---

## Step 4 — Identify the dominant constraint

Common real-world constraints:
- Database lock contention
- N+1 queries under concurrency
- Cache ineffective due to key design
- Thread pool exhaustion
- Network latency amplified by retries

Avoid fixing multiple things at once.

---

## Step 5 — Validate with targeted tests

Use:
- Load tests (k6 / locust)
- Log analysis
- Flame graphs
- Query plans

Goal: confirm the constraint, not guess.

---

## Step 6 — Implement minimal, high-impact fixes

Examples:
- Index change instead of cache layer
- Query rewrite instead of scaling DB
- Async boundary instead of more workers

---

## Step 7 — Measure after & document decisions

Always produce:
- Before/After metrics
- What was changed
- Why this fix was chosen
- What was intentionally not changed

This becomes institutional knowledge.

---

## Deliverables of a proper audit

- Baseline metrics snapshot
- Bottleneck explanation
- Prioritized fix list
- Risk assessment
- Cost vs impact analysis
