# Performance Metrics Baseline

A baseline is the reference point that allows you to **prove improvement**.

---

## Core latency metrics

Always capture:
- P50 (median)
- P95 (user-visible pain)
- P99 (system stress indicator)

Avoid averages — they hide tail latency.

---

## Throughput

- Requests per second (RPS)
- Transactions per second (TPS)

Track throughput alongside latency to detect saturation.

---

## Error metrics

- HTTP 4xx / 5xx rate
- Timeouts
- Retries

Latency without errors is still a failure if users abandon.

---

## Resource metrics

At minimum:
- CPU usage (user/system)
- Memory usage
- Disk IO wait
- Network throughput

Correlate spikes with latency.

---

## Database metrics

- Query latency distribution
- Lock wait time
- Active connections
- Slow query count

High CPU on DB ≠ bottleneck by default.

---

## Cache metrics

- Hit ratio
- Evictions
- Key cardinality
- Serialization cost

Low hit ratio often indicates **design**, not size.

---

## Baseline rules

- Capture during normal traffic
- Capture during peak traffic
- Save raw data
- Timestamp everything
