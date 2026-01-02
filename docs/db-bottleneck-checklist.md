# Database Bottleneck Checklist

> A comprehensive guide for diagnosing and resolving database performance bottlenecks before scaling.

Scaling databases is expensive and often unnecessary if the root cause is inefficient queries, poor indexing, or architectural issues. This checklist provides a systematic approach to identify database bottlenecks and implement cost-effective fixes.

---

## Table of Contents

1. [Query Performance Analysis](#query-performance-analysis)
2. [Index Effectiveness](#index-effectiveness)
3. [Concurrency & Lock Analysis](#concurrency--lock-analysis)
4. [Connection Management](#connection-management)
5. [Data Access Patterns](#data-access-patterns)
6. [Schema & Design Issues](#schema--design-issues)
7. [Scaling Myths & Realities](#scaling-myths--realities)
8. [Evidence Collection](#evidence-collection)
9. [Optimization Strategies](#optimization-strategies)

---

## Query Performance Analysis

### Query Latency Distribution

**Question**: What is the latency distribution of database queries?

**Metrics to Collect**:
- P50 (median) query latency
- P95 query latency (user-visible pain)
- P99 query latency (system stress)
- P99.9 query latency (extreme tail)
- Maximum query latency

**Evaluation Criteria**:
- ✅ **Excellent**: P95 < 10ms, P99 < 50ms
- ✅ **Good**: P95 < 50ms, P99 < 200ms
- ⚠️ **Acceptable**: P95 < 200ms, P99 < 1s
- ❌ **Poor**: P95 > 200ms, P99 > 1s

**Analysis**:
- Identify queries exceeding P95 threshold
- Identify queries with high variance (unpredictable)
- Identify queries that degrade under load
- Correlate query latency with application latency

### Slow Query Identification

**Question**: Which queries are consistently slow?

**Detection Methods**:
- Slow query logs (queries exceeding threshold)
- APM query analysis
- Database query statistics
- Application-level query timing

**Analysis**:
- Frequency of slow queries
- Impact of slow queries (how many requests affected)
- Patterns in slow queries (specific tables, operations)
- Correlation with traffic patterns

**Common Causes**:
- Missing indexes
- Inefficient query plans
- Full table scans
- Complex joins without optimization
- Suboptimal WHERE clauses

### Query Pattern Analysis

**Question**: Are there problematic query patterns?

**Patterns to Identify**:

#### N+1 Query Problem
**Symptoms**:
- Query count scales with result set size
- Many small queries instead of one large query
- High query count per request

**Example**:
```sql
-- Bad: N+1 pattern
SELECT * FROM users WHERE id = 1;
SELECT * FROM orders WHERE user_id = 1;
SELECT * FROM orders WHERE user_id = 2;
-- ... one query per user

-- Good: Single query with JOIN
SELECT u.*, o.* FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.id IN (1, 2, 3, ...);
```

**Detection**:
- Monitor query count per request
- Identify queries executed in loops
- Check for queries in application loops

#### Unbounded Result Sets
**Symptoms**:
- Queries returning large result sets
- Memory pressure from large results
- Network bandwidth consumption

**Example**:
```sql
-- Bad: No LIMIT
SELECT * FROM orders WHERE status = 'pending';

-- Good: Bounded result
SELECT * FROM orders WHERE status = 'pending' LIMIT 100;
```

**Detection**:
- Monitor result set sizes
- Identify queries without LIMIT
- Check for pagination implementation

#### Cartesian Products
**Symptoms**:
- Extremely large result sets
- High memory usage
- Slow query execution

**Example**:
```sql
-- Bad: Missing JOIN condition
SELECT * FROM users, orders;

-- Good: Proper JOIN
SELECT * FROM users u
JOIN orders o ON o.user_id = u.id;
```

### Query Execution Plan Analysis

**Question**: Are queries using optimal execution plans?

**Analysis Tools**:
- `EXPLAIN` (query plan without execution)
- `EXPLAIN ANALYZE` (query plan with actual execution stats)
- Query plan visualization tools

**What to Look For**:
- ✅ Index usage (index scans, index seeks)
- ✅ Join algorithms (hash joins, nested loops, merge joins)
- ✅ Filter pushdown (filters applied early)
- ✅ Sort operations (in-memory vs. disk-based)
- ❌ Full table scans (sequential scans)
- ❌ Missing index warnings
- ❌ High estimated vs. actual row counts

**Red Flags**:
- Full table scans on large tables
- Missing index warnings
- High cost estimates
- Large difference between estimated and actual rows
- Expensive sort operations

---

## Index Effectiveness

### Index Usage Analysis

**Question**: Are indexes actually being used?

**Metrics to Collect**:
- Index usage statistics
- Index scan vs. sequential scan ratio
- Unused indexes
- Missing index recommendations

**Evaluation**:
- Check index usage in query plans
- Monitor index hit ratio
- Identify unused indexes (maintenance overhead)
- Identify missing indexes (performance opportunity)

### Index Design Evaluation

**Question**: Are indexes designed optimally?

**Index Types to Evaluate**:

#### Primary Key Indexes
- ✅ Clustered indexes (usually primary key)
- ✅ Unique constraints
- ✅ Foreign key indexes

#### Secondary Indexes
- ✅ Covering indexes (include all needed columns)
- ✅ Composite indexes (multiple columns)
- ✅ Partial indexes (filtered indexes)

#### Specialized Indexes
- ✅ Full-text indexes (for text search)
- ✅ Spatial indexes (for geospatial data)
- ✅ JSON indexes (for JSONB columns)

**Index Design Principles**:
- Index columns used in WHERE clauses
- Index columns used in JOIN conditions
- Index columns used in ORDER BY
- Consider composite indexes for multiple conditions
- Consider covering indexes to avoid table lookups

### Index Maintenance

**Question**: Are indexes maintained properly?

**Maintenance Tasks**:
- Index statistics updates
- Index fragmentation analysis
- Index rebuild/reorganize
- Unused index removal

**Metrics to Monitor**:
- Index fragmentation percentage
- Index statistics freshness
- Index maintenance overhead
- Index size growth

**Common Issues**:
- ❌ Outdated index statistics (poor query plans)
- ❌ High index fragmentation (slow scans)
- ❌ Unused indexes (wasted space, maintenance overhead)
- ❌ Missing indexes (slow queries)

---

## Concurrency & Lock Analysis

### Lock Wait Time

**Question**: Are queries waiting for locks?

**Metrics to Collect**:
- Average lock wait time
- Maximum lock wait time
- Lock wait time distribution
- Lock wait time trends

**Evaluation Criteria**:
- ✅ **Excellent**: Lock wait time < 1ms
- ✅ **Good**: Lock wait time < 10ms
- ⚠️ **Acceptable**: Lock wait time < 100ms
- ❌ **Poor**: Lock wait time > 100ms

**Analysis**:
- Identify queries with high lock wait time
- Identify tables with frequent lock contention
- Correlate lock wait time with query latency
- Identify lock escalation patterns

### Lock Contention Patterns

**Question**: What types of lock contention occur?

**Lock Types to Monitor**:

#### Row-Level Locks
- **Shared locks** (SELECT queries)
- **Exclusive locks** (UPDATE, DELETE, INSERT)
- **Intent locks** (table-level coordination)

#### Table-Level Locks
- **Schema locks** (DDL operations)
- **Bulk update locks** (large updates)

#### Deadlocks
- Circular wait conditions
- Transaction ordering issues

**Common Contention Scenarios**:
- **Hot rows**: Many transactions updating same rows
- **Long transactions**: Transactions holding locks too long
- **Lock escalation**: Row locks escalating to table locks
- **Deadlocks**: Circular wait conditions

### Transaction Analysis

**Question**: Are transactions holding locks too long?

**Metrics to Collect**:
- Transaction duration
- Lock hold time
- Transaction isolation level
- Transaction rollback rate

**Analysis**:
- Identify long-running transactions
- Identify transactions holding locks unnecessarily
- Check transaction isolation levels
- Identify transaction deadlocks

**Common Issues**:
- ❌ Long-running transactions (holding locks)
- ❌ Unnecessary transaction scope (too broad)
- ❌ Inappropriate isolation levels (too strict)
- ❌ Transaction deadlocks

**Optimization Strategies**:
- Reduce transaction scope
- Use appropriate isolation levels
- Minimize lock hold time
- Use optimistic locking where possible
- Implement retry logic for deadlocks

---

## Connection Management

### Connection Pool Saturation

**Question**: Is the connection pool sized appropriately?

**Metrics to Collect**:
- Active connections
- Idle connections
- Connection pool utilization
- Connection wait time
- Connection errors

**Evaluation Criteria**:
- ✅ Pool utilization < 80% under normal load
- ✅ Connection wait time < 10ms
- ✅ No connection errors
- ⚠️ Pool utilization 80-90% (monitor closely)
- ❌ Pool utilization > 90% (saturation)
- ❌ Connection wait time > 100ms
- ❌ Connection errors occurring

**Common Issues**:
- ❌ Connection pool too small (saturation)
- ❌ Connection pool too large (resource waste)
- ❌ Connection leaks (connections not released)
- ❌ Long-lived connections (holding connections unnecessarily)

### Connection Lifecycle

**Question**: Are connections managed efficiently?

**Analysis**:
- Connection acquisition time
- Connection release time
- Connection lifetime
- Connection reuse patterns

**Best Practices**:
- ✅ Use connection pooling
- ✅ Release connections promptly
- ✅ Set appropriate connection timeouts
- ✅ Monitor connection leaks
- ✅ Use connection pool monitoring

### Thread-Per-Connection Issues

**Question**: Does the database use thread-per-connection model?

**Analysis**:
- Thread count per connection
- Thread overhead
- Context switching overhead
- Scalability limitations

**Issues**:
- ❌ High thread overhead (memory per thread)
- ❌ Context switching overhead
- ❌ Limited scalability (thread limits)
- ❌ Resource waste (idle threads)

**Solutions**:
- Use connection pooling
- Use async I/O where possible
- Consider connection multiplexing
- Use thread pools efficiently

---

## Data Access Patterns

### Hot Rows / Hot Keys

**Question**: Are there hot rows causing contention?

**Detection**:
- Identify frequently accessed rows
- Identify frequently updated rows
- Monitor lock contention on specific rows
- Analyze access patterns

**Common Hot Row Scenarios**:
- **Counters**: Frequently updated counters
- **Sequences**: ID generation sequences
- **Configuration**: Frequently read configuration
- **Leader election**: Distributed system coordination

**Solutions**:
- **Sharding**: Distribute hot rows across shards
- **Caching**: Cache hot rows in application
- **Denormalization**: Reduce need for hot row access
- **Optimistic locking**: Reduce lock contention
- **Batch updates**: Reduce update frequency

### Unbounded Scans

**Question**: Are there queries scanning entire tables?

**Detection**:
- Identify queries with full table scans
- Monitor sequential scan operations
- Analyze query plans for scans
- Check for missing indexes

**Common Causes**:
- Missing indexes
- Inefficient WHERE clauses
- Unbounded result sets
- Poor query design

**Solutions**:
- Add appropriate indexes
- Optimize WHERE clauses
- Add LIMIT clauses
- Use pagination
- Consider partitioning

### JSON Field Filtering

**Question**: Are JSON fields used as filters inefficiently?

**Analysis**:
- Identify queries filtering on JSON fields
- Check for JSON index usage
- Analyze JSON query performance
- Evaluate JSON field access patterns

**Common Issues**:
- ❌ No indexes on JSON fields
- ❌ Full table scans for JSON queries
- ❌ Inefficient JSON path queries
- ❌ JSON field extraction overhead

**Solutions**:
- Add JSON indexes (GIN indexes for JSONB)
- Use JSON path indexes
- Consider denormalization for frequently accessed fields
- Optimize JSON query patterns

---

## Schema & Design Issues

### Normalization vs. Denormalization

**Question**: Is the schema appropriately normalized/denormalized?

**Analysis**:
- Evaluate normalization level
- Identify denormalization opportunities
- Analyze join complexity
- Evaluate query performance impact

**Trade-offs**:
- **Normalization**: Reduces redundancy, increases joins
- **Denormalization**: Increases redundancy, reduces joins

**Guidelines**:
- Normalize for write-heavy, consistency-critical data
- Denormalize for read-heavy, performance-critical queries
- Consider materialized views for complex queries
- Use read replicas for read-heavy workloads

### Data Type Optimization

**Question**: Are data types optimal for storage and performance?

**Analysis**:
- Evaluate data type sizes
- Check for oversized data types
- Analyze storage efficiency
- Evaluate index efficiency

**Common Issues**:
- ❌ Using VARCHAR(255) for small strings
- ❌ Using BIGINT for small integers
- ❌ Using TEXT for short strings
- ❌ Using JSON for structured data (consider JSONB)

**Optimization**:
- Use appropriate data type sizes
- Use fixed-length types where possible
- Consider compression for large text fields
- Use JSONB instead of JSON (PostgreSQL)

### Partitioning

**Question**: Would partitioning improve performance?

**Analysis**:
- Evaluate table size
- Analyze access patterns
- Identify partition key candidates
- Evaluate partition maintenance overhead

**Partitioning Strategies**:
- **Range partitioning**: By date ranges, ID ranges
- **List partitioning**: By category, region
- **Hash partitioning**: For even distribution

**Benefits**:
- Improved query performance (partition pruning)
- Easier maintenance (partition-level operations)
- Better scalability (partition-level scaling)

**Considerations**:
- Partition key selection
- Partition maintenance overhead
- Query pattern compatibility
- Cross-partition query performance

---

## Scaling Myths & Realities

### Myth 1: Bigger Instance Fixes Bad Queries

**Reality**: Vertical scaling (bigger instance) may help temporarily, but:
- ❌ Doesn't fix inefficient queries
- ❌ Doesn't fix missing indexes
- ❌ Doesn't fix lock contention
- ❌ Expensive and has limits
- ✅ Fix queries first, then scale if needed

### Myth 2: Read Replicas Fix Write Contention

**Reality**: Read replicas help with read scaling, but:
- ❌ Don't fix write contention
- ❌ Don't fix lock contention on primary
- ❌ Add complexity (replication lag, consistency)
- ✅ Use for read-heavy workloads, not write issues

### Myth 3: Cache Replaces Indexes

**Reality**: Caching and indexing serve different purposes:
- ❌ Cache doesn't help with writes
- ❌ Cache doesn't help with range queries
- ❌ Cache adds complexity and consistency issues
- ✅ Use both: indexes for queries, cache for hot data

### Myth 4: More Connections = Better Performance

**Reality**: More connections can actually hurt:
- ❌ Connection overhead (memory, threads)
- ❌ Lock contention increases
- ❌ Context switching overhead
- ✅ Optimal connection pool size is key

### Myth 5: Horizontal Scaling Always Better

**Reality**: Horizontal scaling has trade-offs:
- ❌ Adds complexity (sharding, routing)
- ❌ May not help with single-query performance
- ❌ Transaction complexity across shards
- ✅ Use when vertical scaling insufficient

---

## Evidence Collection

### Query Plan Analysis

**Tools**:
- `EXPLAIN` / `EXPLAIN ANALYZE` (PostgreSQL, MySQL)
- `SHOW PLAN` (SQL Server)
- Query plan visualization tools

**What to Collect**:
- Execution plans for slow queries
- Index usage in plans
- Estimated vs. actual row counts
- Cost estimates
- Operation types (scans, joins, sorts)

### Query Latency Histograms

**Metrics**:
- Query latency distribution (P50, P95, P99)
- Query latency over time
- Query latency by query type
- Query latency correlation with load

**Tools**:
- APM tools (New Relic, Datadog)
- Database monitoring tools
- Application-level metrics
- Custom instrumentation

### Lock Analysis

**Metrics**:
- Lock wait time distribution
- Lock wait time by table
- Lock wait time by query type
- Deadlock frequency
- Lock escalation events

**Tools**:
- Database lock monitoring
- Query lock analysis
- Deadlock detection logs
- Lock wait graphs

### Slow Query Logs

**What to Collect**:
- Queries exceeding threshold
- Query execution time
- Query frequency
- Query patterns
- Query context (user, application)

**Analysis**:
- Identify most frequent slow queries
- Identify most expensive slow queries
- Identify query patterns
- Correlate with application behavior

### Database Statistics

**Metrics**:
- Table sizes and growth
- Index sizes and usage
- Connection statistics
- Transaction statistics
- Cache/buffer statistics

**Tools**:
- Database system tables
- Database monitoring tools
- Custom queries for statistics

---

## Optimization Strategies

### Query Optimization

**Strategies**:
1. **Add missing indexes**: Based on query patterns
2. **Optimize query plans**: Use hints if necessary
3. **Rewrite queries**: More efficient formulations
4. **Use appropriate JOIN types**: INNER vs. LEFT vs. RIGHT
5. **Optimize WHERE clauses**: Push filters early
6. **Use LIMIT clauses**: Bound result sets
7. **Avoid SELECT ***: Select only needed columns

### Index Optimization

**Strategies**:
1. **Add covering indexes**: Include all needed columns
2. **Create composite indexes**: For multi-column queries
3. **Remove unused indexes**: Reduce maintenance overhead
4. **Rebuild fragmented indexes**: Improve scan performance
5. **Update statistics**: Ensure optimal query plans

### Connection Optimization

**Strategies**:
1. **Right-size connection pools**: Based on load
2. **Use connection pooling**: Efficient connection reuse
3. **Implement connection timeouts**: Prevent leaks
4. **Monitor connection usage**: Identify issues early
5. **Use async I/O**: Where supported

### Transaction Optimization

**Strategies**:
1. **Reduce transaction scope**: Minimize lock hold time
2. **Use appropriate isolation levels**: Balance consistency and performance
3. **Implement optimistic locking**: Reduce lock contention
4. **Batch operations**: Reduce transaction count
5. **Avoid long-running transactions**: Keep transactions short

### Schema Optimization

**Strategies**:
1. **Denormalize hot paths**: Reduce join complexity
2. **Partition large tables**: Improve query performance
3. **Optimize data types**: Reduce storage and improve performance
4. **Use materialized views**: For complex queries
5. **Consider read replicas**: For read-heavy workloads

---

## Checklist Summary

Use this checklist before scaling your database:

### Query Performance
- [ ] Query latency distribution analyzed (P50, P95, P99)
- [ ] Slow queries identified and analyzed
- [ ] Query patterns evaluated (N+1, unbounded scans)
- [ ] Query execution plans reviewed
- [ ] Query optimization opportunities identified

### Index Effectiveness
- [ ] Index usage analyzed
- [ ] Missing indexes identified
- [ ] Unused indexes identified
- [ ] Index design evaluated
- [ ] Index maintenance performed

### Concurrency & Locks
- [ ] Lock wait time analyzed
- [ ] Lock contention patterns identified
- [ ] Transaction analysis performed
- [ ] Deadlocks investigated
- [ ] Lock optimization opportunities identified

### Connection Management
- [ ] Connection pool sizing evaluated
- [ ] Connection pool utilization monitored
- [ ] Connection leaks identified
- [ ] Connection lifecycle analyzed
- [ ] Connection optimization performed

### Data Access Patterns
- [ ] Hot rows/keys identified
- [ ] Unbounded scans found
- [ ] JSON field usage evaluated
- [ ] Access patterns analyzed
- [ ] Optimization opportunities identified

### Schema & Design
- [ ] Normalization level evaluated
- [ ] Data types optimized
- [ ] Partitioning considered
- [ ] Schema design reviewed
- [ ] Optimization opportunities identified

### Evidence Collection
- [ ] Query plans collected and analyzed
- [ ] Query latency histograms created
- [ ] Lock analysis performed
- [ ] Slow query logs analyzed
- [ ] Database statistics collected

---

## Decision Framework

After completing this checklist, use this framework to decide next steps:

### If Queries Are Slow
1. **Add missing indexes** (high impact, low risk)
2. **Optimize query plans** (medium impact, low risk)
3. **Rewrite queries** (high impact, medium risk)
4. **Consider denormalization** (high impact, high risk)

### If Locks Are Contended
1. **Reduce transaction scope** (high impact, low risk)
2. **Use appropriate isolation levels** (medium impact, low risk)
3. **Implement optimistic locking** (high impact, medium risk)
4. **Shard hot rows** (high impact, high risk)

### If Connections Are Saturated
1. **Right-size connection pools** (high impact, low risk)
2. **Fix connection leaks** (high impact, low risk)
3. **Use connection pooling** (high impact, low risk)
4. **Consider read replicas** (medium impact, medium risk)

### If Schema Is Inefficient
1. **Optimize data types** (medium impact, low risk)
2. **Add appropriate indexes** (high impact, low risk)
3. **Consider partitioning** (high impact, high risk)
4. **Denormalize hot paths** (high impact, high risk)

### Only After Optimization
- Consider vertical scaling (bigger instance)
- Consider horizontal scaling (read replicas, sharding)
- Consider caching layer
- Consider database migration

---

## Next Steps

After completing this checklist:

1. **Document findings**: Record all issues and metrics
2. **Prioritize fixes**: Rank by impact, effort, and risk
3. **Implement optimizations**: Start with high-impact, low-risk fixes
4. **Measure impact**: Compare before/after metrics
5. **Re-evaluate**: Determine if scaling is still needed
