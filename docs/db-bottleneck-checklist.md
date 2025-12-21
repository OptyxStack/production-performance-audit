# Database Bottleneck Checklist

Use this checklist before scaling your database.

---

## Query behavior

- Are there queries > P95 latency?
- Are indexes actually used?
- Any N+1 patterns under concurrency?

---

## Concurrency & locks

- Lock wait time increasing?
- Long transactions holding locks?
- Read queries blocked by writes?

---

## Connection management

- Connection pool saturation?
- Too many idle connections?
- Thread per connection issues?

---

## Data access patterns

- Hot rows or hot keys?
- Unbounded scans?
- JSON fields used as filters?

---

## Scaling myths

Do NOT assume:
- Bigger instance fixes bad queries
- Read replicas fix write contention
- Cache replaces indexes

---

## Evidence to collect

- EXPLAIN / EXPLAIN ANALYZE
- Query latency histograms
- Lock graphs
- Slow query logs
