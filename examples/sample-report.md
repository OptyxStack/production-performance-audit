# Sample Performance Audit Report

System: E-commerce checkout service

---

## Executive summary

Checkout latency spikes were caused by database lock contention during order creation.

---

## Baseline

- P95 latency: 2.4s
- Error rate: 1.8%
- CPU: stable

---

## Bottleneck

A single table experienced row-level locks under concurrent writes.

---

## Fix

- Reduced transaction scope
- Added supporting index

---

## Results

- P95 latency reduced to 620ms
- Error rate < 0.2%

---

## Recommendation

Proceed with controlled traffic increase. No horizontal scaling required.
