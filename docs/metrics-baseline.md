# Performance Metrics Baseline

> A comprehensive guide for establishing quantitative baselines that enable evidence-based performance improvements.

A baseline is the **quantitative reference point** that allows you to prove improvement, distinguish signal from noise, and make data-driven decisions. Without a proper baseline, you cannot measure the impact of changes or validate optimizations.

---

## Table of Contents

1. [Why Baselines Matter](#why-baselines-matter)
2. [Baseline Collection Methodology](#baseline-collection-methodology)
3. [Core Application Metrics](#core-application-metrics)
4. [Infrastructure Metrics](#infrastructure-metrics)
5. [Database Metrics](#database-metrics)
6. [Cache Metrics](#cache-metrics)
7. [Statistical Validation](#statistical-validation)
8. [Baseline Documentation](#baseline-documentation)
9. [Common Pitfalls](#common-pitfalls)

---

## Why Baselines Matter

### The Problem Without Baselines

Without a baseline, you cannot:
- **Prove improvements**: Did changes actually help?
- **Detect regressions**: Did changes make things worse?
- **Distinguish signal from noise**: Is variation normal or significant?
- **Make data-driven decisions**: What should we optimize?
- **Justify investments**: What's the ROI of optimizations?

### What a Baseline Provides

A proper baseline enables:
- ✅ **Quantitative comparison**: Before/after metrics
- ✅ **Statistical significance**: Confidence in improvements
- ✅ **Trend analysis**: Performance over time
- ✅ **Anomaly detection**: Identify unusual behavior
- ✅ **Capacity planning**: Model future needs

### Baseline Principles

1. **Establish before changes**: Never modify system before baseline
2. **Comprehensive coverage**: Capture all relevant metrics
3. **Statistical validity**: Sufficient sample size and time period
4. **Representative conditions**: Normal and peak traffic
5. **Documentation**: Record all conditions and assumptions

---

## Baseline Collection Methodology

### Collection Period

**Minimum Requirements**:
- **24 hours**: Capture daily patterns
- **7 days**: Capture weekly patterns (recommended)
- **30 days**: Capture monthly patterns (for capacity planning)

**Why Longer Periods**:
- Daily patterns (morning rush, lunch breaks)
- Weekly patterns (weekday vs. weekend)
- Seasonal patterns (holidays, events)
- Traffic variations (marketing campaigns)

### Collection Frequency

**Metric-Specific Frequencies**:

**High-Frequency Metrics** (1-5 second intervals):
- CPU usage
- Memory usage
- Request latency
- Active connections
- Queue depth

**Medium-Frequency Metrics** (10-30 second intervals):
- Throughput (RPS, QPS)
- Error rates
- Cache hit ratios
- Database query rates

**Low-Frequency Metrics** (1-5 minute intervals):
- Database statistics
- Cache statistics
- Disk I/O statistics
- Network statistics

### Collection Conditions

**Normal Traffic Baseline**:
- Capture during typical business hours
- Exclude anomalies (incidents, deployments)
- Representative of normal operation
- Multiple samples across time periods

**Peak Traffic Baseline**:
- Capture during known peak periods
- Include traffic spikes
- Representative of maximum load
- Critical for capacity planning

**Special Conditions**:
- Document any special circumstances
- Marketing campaigns
- External API issues
- Infrastructure changes
- Deployment events

### Statistical Validation

**Sample Size Requirements**:
- Sufficient data points for statistical significance
- Minimum 1000 samples per metric
- More samples for higher confidence

**Outlier Detection**:
- Identify and exclude anomalies
- Document outlier reasons
- Don't exclude valid extreme values (P99, P99.9)

**Traffic Pattern Validation**:
- Confirm baseline period is representative
- Compare with historical patterns
- Validate against business metrics

---

## Core Application Metrics

### Latency Distribution

**Why Percentiles, Not Averages**:

Averages hide tail latency. Consider:
- 99 requests at 10ms
- 1 request at 10,000ms
- Average: 109ms (misleading)
- P95: 10ms (accurate for most users)
- P99: 10,000ms (accurate for worst-case)

**Required Percentiles**:

**P50 (Median)**:
- Typical user experience
- 50% of requests faster than this
- Less affected by outliers

**P95**:
- User-visible pain threshold
- 95% of requests faster than this
- Critical for user experience

**P99**:
- System stress indicator
- 99% of requests faster than this
- Identifies tail latency issues

**P99.9**:
- Extreme tail events
- 99.9% of requests faster than this
- Identifies rare but critical issues

**Max**:
- Worst-case scenario
- Absolute maximum latency
- Useful for identifying outliers

**Collection Method**:
```javascript
// Example: Collecting latency percentiles
const latencies = []; // Array of request latencies

// After collecting samples
latencies.sort((a, b) => a - b);
const p50 = latencies[Math.floor(latencies.length * 0.50)];
const p95 = latencies[Math.floor(latencies.length * 0.95)];
const p99 = latencies[Math.floor(latencies.length * 0.99)];
const p99_9 = latencies[Math.floor(latencies.length * 0.999)];
```

### Throughput Metrics

**Requests per Second (RPS)**:
- Total requests per second
- Requests per second by endpoint
- Requests per second trends
- Peak vs. average RPS

**Queries per Second (QPS)**:
- Database queries per second
- Queries per second by query type
- Read vs. write QPS
- Query rate trends

**Transactions per Second (TPS)**:
- Business transactions per second
- Transaction rate by type
- Transaction success rate
- Transaction latency

**Collection**:
- Aggregate over time windows (1s, 10s, 1m)
- Track trends over time
- Correlate with latency
- Identify saturation points

### Error Metrics

**HTTP Status Codes**:
- **2xx**: Success rate
- **4xx**: Client error rate (may indicate test issues)
- **5xx**: Server error rate (critical)
- **Timeouts**: Request timeout rate
- **Connection errors**: Connection failure rate

**Error Rate Calculation**:
```
Error Rate = (Failed Requests) / (Total Requests)
```

**Error Types**:
- **Transient errors**: Temporary failures (retries may help)
- **Persistent errors**: Systematic failures (needs investigation)
- **Cascading errors**: Errors causing more errors

**Collection**:
- Error rate overall
- Error rate by endpoint
- Error rate by error type
- Error rate trends
- Error correlation with load

### Request Mix

**Endpoint Distribution**:
- Requests per endpoint
- Latency per endpoint
- Error rate per endpoint
- Resource usage per endpoint

**Request Types**:
- Read vs. write ratio
- GET vs. POST ratio
- Simple vs. complex requests
- Cached vs. uncached requests

**Collection**:
- Track request distribution
- Identify hot endpoints
- Identify problematic endpoints
- Correlate with performance

---

## Infrastructure Metrics

### CPU Metrics

**CPU Utilization**:
- **User CPU**: Application processing
- **System CPU**: Kernel operations
- **I/O Wait**: Waiting for I/O operations
- **Steal Time**: Virtualization overhead (cloud)
- **Idle Time**: Unused CPU capacity

**Load Average**:
- **1-minute average**: Short-term load
- **5-minute average**: Medium-term load
- **15-minute average**: Long-term load
- **Per-core load**: Load per CPU core

**Collection**:
- Sample every 1-5 seconds
- Track trends over time
- Correlate with latency
- Identify CPU-bound bottlenecks

**Evaluation**:
- ✅ **Healthy**: CPU < 70% utilization
- ⚠️ **Warning**: CPU 70-85% utilization
- ❌ **Critical**: CPU > 85% utilization

### Memory Metrics

**Memory Usage**:
- **Total memory**: System total
- **Used memory**: Currently in use
- **Available memory**: Free for use
- **Cached memory**: File system cache
- **Buffered memory**: Kernel buffers

**Memory Pressure**:
- **Swap usage**: Disk swap usage
- **Swap activity**: Swap in/out rate
- **OOM kills**: Out-of-memory kills
- **Memory leaks**: Gradual memory growth

**Collection**:
- Sample every 1-5 seconds
- Track memory trends
- Monitor for leaks
- Correlate with performance

**Evaluation**:
- ✅ **Healthy**: Memory < 80% utilization, no swap
- ⚠️ **Warning**: Memory 80-90%, minimal swap
- ❌ **Critical**: Memory > 90%, high swap activity

### Disk I/O Metrics

**I/O Operations**:
- **Read IOPS**: Read operations per second
- **Write IOPS**: Write operations per second
- **Total IOPS**: Combined operations

**I/O Latency**:
- **Read latency**: Time to read from disk
- **Write latency**: Time to write to disk
- **I/O wait time**: CPU waiting for I/O

**I/O Throughput**:
- **Read throughput**: Bytes read per second
- **Write throughput**: Bytes written per second
- **Total throughput**: Combined throughput

**Collection**:
- Sample every 10-30 seconds
- Track I/O patterns
- Identify I/O-bound bottlenecks
- Correlate with latency

**Evaluation**:
- ✅ **Healthy**: Low I/O wait, reasonable latency
- ⚠️ **Warning**: Moderate I/O wait, increasing latency
- ❌ **Critical**: High I/O wait, high latency

### Network Metrics

**Network Throughput**:
- **Bytes in**: Incoming network traffic
- **Bytes out**: Outgoing network traffic
- **Packets in**: Incoming packets
- **Packets out**: Outgoing packets

**Network Latency**:
- **Round-trip time (RTT)**: Network latency
- **Packet loss**: Lost packets
- **Retransmissions**: Retransmitted packets

**Connection Metrics**:
- **Active connections**: Current connections
- **Connection rate**: New connections per second
- **Connection errors**: Connection failures

**Collection**:
- Sample every 10-30 seconds
- Track network patterns
- Identify network bottlenecks
- Correlate with latency

---

## Database Metrics

### Query Performance

**Query Latency Distribution**:
- P50, P95, P99, P99.9 query latency
- Query latency by query type
- Query latency trends
- Query latency correlation with load

**Slow Queries**:
- Queries exceeding threshold (e.g., > 100ms)
- Slow query frequency
- Slow query patterns
- Slow query impact

**Query Execution Plans**:
- Index usage
- Full table scans
- Join algorithms
- Sort operations

**Collection**:
- Query logs
- Database statistics
- APM query analysis
- Slow query logs

### Lock Contention

**Lock Wait Time**:
- Average lock wait time
- Maximum lock wait time
- Lock wait time distribution
- Lock wait time trends

**Lock Types**:
- Row-level locks
- Table-level locks
- Deadlocks
- Lock escalation

**Collection**:
- Database lock monitoring
- Query lock analysis
- Deadlock detection logs

### Connection Management

**Connection Pool**:
- Active connections
- Idle connections
- Connection pool utilization
- Connection wait time

**Connection Errors**:
- Connection failures
- Connection timeouts
- Connection pool exhaustion

**Collection**:
- Connection pool metrics
- Database connection logs
- Application connection metrics

### Database Resource Usage

**CPU Usage**:
- Database CPU utilization
- Query CPU usage
- Background process CPU

**Memory Usage**:
- Buffer pool usage
- Query cache usage
- Connection memory

**I/O Usage**:
- Database disk I/O
- Log file I/O
- Data file I/O

**Collection**:
- Database system tables
- Database monitoring tools
- Infrastructure metrics

---

## Cache Metrics

### Hit Ratio

**Overall Hit Ratio**:
```
Hit Ratio = (Cache Hits) / (Cache Hits + Cache Misses)
```

**Hit Ratio by Pattern**:
- Hit ratio per endpoint
- Hit ratio per key pattern
- Hit ratio by data type

**Hit Ratio Trends**:
- Hit ratio over time
- Hit ratio during peak vs. normal
- Hit ratio correlation with load

**Collection**:
- Cache statistics
- Application metrics
- Cache monitoring tools

**Evaluation**:
- ✅ **Excellent**: Hit ratio > 90%
- ✅ **Good**: Hit ratio 70-90%
- ⚠️ **Acceptable**: Hit ratio 50-70%
- ❌ **Poor**: Hit ratio < 50%

### Cache Performance

**Cache Operation Latency**:
- Cache lookup latency
- Cache write latency
- Cache delete latency

**Cache Evictions**:
- Eviction rate
- Eviction reasons (TTL, memory pressure)
- Eviction patterns

**Cache Memory Usage**:
- Total cache memory
- Memory per key
- Memory trends

**Collection**:
- Cache statistics
- Application metrics
- Cache monitoring tools

### Cache Effectiveness

**Work Avoided**:
- Database queries avoided
- API calls avoided
- Computations avoided

**Cost-Benefit**:
- Cache memory cost
- Cache CPU overhead
- Database load reduction
- Overall cost-benefit

**Collection**:
- Compare with/without cache
- Measure database load reduction
- Calculate cost savings

---

## Statistical Validation

### Sample Size Requirements

**Minimum Sample Size**:
- **1000 samples**: Basic statistical validity
- **10,000 samples**: Good statistical validity
- **100,000+ samples**: High confidence

**Time Period Requirements**:
- **24 hours**: Daily patterns
- **7 days**: Weekly patterns (recommended)
- **30 days**: Monthly patterns

### Outlier Detection

**Identifying Outliers**:
- Statistical methods (Z-score, IQR)
- Domain knowledge (known anomalies)
- Visual inspection (histograms, time series)

**Handling Outliers**:
- **Exclude**: If clearly anomalous (deployments, incidents)
- **Include**: If valid extreme values (P99, P99.9)
- **Document**: Record all decisions

### Statistical Significance

**Confidence Intervals**:
- Calculate confidence intervals for metrics
- Use appropriate confidence level (95%, 99%)
- Report uncertainty in measurements

**Trend Analysis**:
- Identify trends over time
- Distinguish trends from noise
- Validate trend significance

### Baseline Validation

**Representativeness**:
- Compare with historical data
- Validate against business metrics
- Confirm normal operation conditions

**Completeness**:
- All required metrics captured
- Sufficient time period
- Sufficient sample size
- No missing data

---

## Baseline Documentation

### Required Documentation

**Baseline Metadata**:
- **Timestamp range**: Start and end times
- **Collection period**: Duration of collection
- **Collection frequency**: Sampling intervals
- **Environment**: Staging, production, etc.

**System State**:
- **Application version**: Code version
- **Configuration**: System configuration
- **Infrastructure**: Instance types, sizes
- **Deployment**: Deployment details

**Traffic Characteristics**:
- **Request rate**: RPS, QPS
- **Request mix**: Endpoint distribution
- **Concurrent users**: Active users
- **Traffic patterns**: Daily/weekly patterns

**External Factors**:
- **Marketing campaigns**: Traffic spikes
- **External API issues**: Third-party problems
- **Infrastructure changes**: System modifications
- **Incidents**: Known issues during collection

### Baseline Report Structure

**Executive Summary**:
- Key metrics overview
- System health assessment
- Notable findings

**Detailed Metrics**:
- All collected metrics
- Percentiles and distributions
- Trends and patterns
- Correlations

**Analysis**:
- Metric interpretation
- Bottleneck identification
- Performance characteristics
- Recommendations

**Raw Data**:
- Store raw metric data
- Timestamp all data points
- Enable future analysis
- Support reproducibility

---

## Common Pitfalls

### Pitfall 1: Insufficient Collection Period

**Problem**: Too short collection period  
**Impact**: Missing patterns, unrepresentative baseline  
**Solution**: Collect for minimum 24 hours, preferably 7 days

### Pitfall 2: Using Averages Instead of Percentiles

**Problem**: Averages hide tail latency  
**Impact**: Missing user-visible performance issues  
**Solution**: Always use P50, P95, P99, P99.9

### Pitfall 3: Not Documenting Conditions

**Problem**: Unknown factors affecting baseline  
**Impact**: Invalid comparisons, incorrect conclusions  
**Solution**: Document all conditions and assumptions

### Pitfall 4: Excluding Valid Extreme Values

**Problem**: Removing P99, P99.9 values as outliers  
**Impact**: Missing tail latency issues  
**Solution**: Only exclude clearly anomalous values

### Pitfall 5: Not Validating Representativeness

**Problem**: Baseline doesn't represent normal operation  
**Impact**: Invalid baseline, incorrect comparisons  
**Solution**: Validate against historical data and business metrics

### Pitfall 6: Incomplete Metric Coverage

**Problem**: Missing critical metrics  
**Impact**: Incomplete picture, missed bottlenecks  
**Solution**: Comprehensive metric collection

### Pitfall 7: Not Saving Raw Data

**Problem**: Only summary statistics saved  
**Impact**: Cannot re-analyze, limited insights  
**Solution**: Save raw data for future analysis

---

## Baseline Checklist

Use this checklist to ensure comprehensive baseline collection:

### Collection Setup
- [ ] Collection period defined (minimum 24 hours)
- [ ] Collection frequency set (appropriate for each metric)
- [ ] Collection tools configured
- [ ] Storage for raw data prepared

### Application Metrics
- [ ] Latency percentiles (P50, P95, P99, P99.9)
- [ ] Throughput (RPS, QPS, TPS)
- [ ] Error rates (4xx, 5xx, timeouts)
- [ ] Request mix (endpoint distribution)

### Infrastructure Metrics
- [ ] CPU usage (user, system, I/O wait)
- [ ] Memory usage (used, available, swap)
- [ ] Disk I/O (IOPS, latency, throughput)
- [ ] Network (throughput, latency, connections)

### Database Metrics
- [ ] Query latency distribution
- [ ] Slow query identification
- [ ] Lock wait time
- [ ] Connection pool utilization

### Cache Metrics
- [ ] Hit ratio (overall and by pattern)
- [ ] Cache operation latency
- [ ] Cache evictions
- [ ] Cache memory usage

### Validation
- [ ] Sufficient sample size
- [ ] Representative time period
- [ ] Outliers identified and handled
- [ ] Statistical validity confirmed

### Documentation
- [ ] Baseline metadata documented
- [ ] System state recorded
- [ ] Traffic characteristics captured
- [ ] External factors noted
- [ ] Raw data saved

---

## Next Steps

After establishing baseline:

1. **Analyze baseline**: Identify patterns and bottlenecks
2. **Document findings**: Record all observations
3. **Set targets**: Define improvement goals
4. **Plan optimizations**: Prioritize fixes
5. **Implement changes**: Apply optimizations
6. **Re-measure**: Compare with baseline
7. **Iterate**: Continue optimizing
