# Production Performance Audit Toolkit

> Find what actually limits your production system — before you scale the wrong thing.

This repository is a **practical, evidence-first toolkit** for auditing performance issues in real production systems.

It is designed for teams who already “monitor everything” — but still don’t know **why the system slows down, breaks under load, or keeps getting more expensive**.

---

## Who this is for

- CTOs and tech leads responsible for production reliability
- Founders of growing products hitting scaling limits
- Senior engineers investigating latency, bottlenecks, or instability

If your system:
- works fine in staging
- passes basic monitoring checks
- but degrades under real traffic

this toolkit is for you.

---

## What this toolkit helps you diagnose

This repo focuses on **real bottlenecks**, not surface metrics.

Common problems it helps uncover:

- P95 / P99 latency spikes under concurrency  
- High CPU but low throughput  
- Databases that “scale vertically” forever without improving latency  
- Caches that exist but don’t actually reduce work  
- Systems that get slower after every new feature  

---

## What a performance audit actually is

A real performance audit is **not**:
- Checking CPU and memory once
- Running Lighthouse or PageSpeed only
- Guessing based on experience

A real audit answers one question clearly:

> **What constraint is limiting this system today, and what decision should we make next?**

This toolkit is structured around that question.

---

## Audit workflow (high level)

1. Define the **business-level symptom**
2. Establish a **metrics baseline** (before touching anything)
3. Map the **critical request path**
4. Identify the **dominant constraint**
5. Validate with **targeted tests**
6. Apply **minimal, high-impact fixes**
7. Measure **before / after** and document decisions

Each step is documented in detail in `/docs`.

---

## Repository structure

