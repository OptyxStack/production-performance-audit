# Caching Effectiveness Checklist

Caching only helps if it reduces real work.

---

## Cache design

- Are keys stable?
- Is TTL appropriate?
- Is cache invalidation explicit?

---

## Hit ratio analysis

- Overall hit ratio
- Hit ratio per endpoint
- Hit ratio under load

High traffic with low hit ratio = wasted memory.

---

## Serialization cost

- Payload size
- CPU spent encoding/decoding
- Compression overhead

Sometimes cache is slower than DB.

---

## Failure modes

- Cache stampede
- Cold start storms
- Thundering herd

---

## Questions to answer

- What work is actually avoided?
- What breaks if cache is bypassed?
- Is cache masking deeper issues?
