# Load Testing with k6

> A comprehensive guide for conducting production-safe, hypothesis-driven load testing.

Load testing is a critical tool for validating performance hypotheses and identifying system limits. This guide focuses on using k6 (and principles applicable to other tools) to conduct effective, production-safe load tests that provide actionable insights.

---

## Table of Contents

1. [Load Testing Philosophy](#load-testing-philosophy)
2. [Test Design Principles](#test-design-principles)
3. [k6 Setup & Configuration](#k6-setup--configuration)
4. [Load Patterns & Scenarios](#load-patterns--scenarios)
5. [Metrics & Monitoring](#metrics--monitoring)
6. [Result Interpretation](#result-interpretation)
7. [Production-Safe Testing](#production-safe-testing)
8. [Advanced Techniques](#advanced-techniques)
9. [Common Mistakes & Pitfalls](#common-mistakes--pitfalls)

---

## Load Testing Philosophy

### Purpose of Load Testing

Load tests should **validate hypotheses**, not satisfy curiosity. Every load test should answer a specific question:

- "Can the system handle 2x current traffic?"
- "What is the maximum throughput before errors increase?"
- "Does the database become the bottleneck at 1000 RPS?"
- "How does latency degrade as concurrency increases?"

### Load Testing vs. Other Testing Types

**Load Testing**: Testing system behavior under expected load  
**Stress Testing**: Testing system behavior beyond expected load  
**Spike Testing**: Testing system response to sudden load increases  
**Endurance Testing**: Testing system behavior over extended periods  
**Capacity Testing**: Finding maximum capacity before degradation

### Key Principles

1. **Hypothesis-Driven**: Test specific hypotheses, not everything
2. **Incremental**: Start small, increase gradually
3. **Production-Safe**: Never impact production users
4. **Measurable**: Define clear success/failure criteria
5. **Repeatable**: Tests should be reproducible
6. **Documented**: Record all test parameters and results

---

## Test Design Principles

### What to Test

**Focus Areas**:
- ✅ **One critical user journey**: Most important user flow
- ✅ **One bottleneck hypothesis**: Specific constraint being tested
- ✅ **One saturation point**: Where system degrades
- ✅ **One optimization**: Before/after comparison

**Avoid**:
- ❌ Testing everything at once (confounding variables)
- ❌ Testing unrealistic scenarios
- ❌ Testing without clear objectives
- ❌ Testing without baseline comparison

### Test Scope Definition

**Define**:
- **User journey**: Specific endpoints/flows to test
- **Load characteristics**: RPS, concurrent users, request mix
- **Success criteria**: Acceptable latency, error rate, throughput
- **Failure criteria**: When to stop test (error threshold)

**Example Test Scope**:
```
Objective: Validate checkout flow can handle 500 RPS
User Journey: Add to cart → Checkout → Payment
Load: 500 RPS sustained for 5 minutes
Success: P95 latency < 500ms, error rate < 0.1%
Failure: Error rate > 1% or P95 latency > 2s
```

### Test Environment

**Environment Selection**:
- **Staging**: Most similar to production
- **Production-like**: Same infrastructure, different data
- **Dedicated test environment**: Isolated from other testing
- **Production (canary)**: Small percentage of real traffic

**Environment Requirements**:
- Same infrastructure as production
- Same database size and characteristics
- Same network topology
- Same application configuration
- Representative data volumes

---

## k6 Setup & Configuration

### Installation

**Install k6**:
```bash
# macOS
brew install k6

# Linux (Debian/Ubuntu)
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# Docker
docker pull grafana/k6
```

### Basic Test Structure

**Minimal k6 Test**:
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },   // Ramp up to 20 users
    { duration: '1m', target: 20 },     // Stay at 20 users
    { duration: '30s', target: 0 },     // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],     // Error rate < 1%
  },
};

export default function () {
  const response = http.get('https://api.example.com/endpoint');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

### Configuration Options

**Key Options**:
```javascript
export const options = {
  // VUs (Virtual Users) and duration
  vus: 10,                    // Number of virtual users
  duration: '30s',            // Test duration
  
  // Stages (ramp-up/ramp-down)
  stages: [
    { duration: '1m', target: 50 },   // Ramp to 50 VUs over 1 minute
    { duration: '3m', target: 50 },   // Stay at 50 VUs for 3 minutes
    { duration: '1m', target: 100 },  // Ramp to 100 VUs over 1 minute
    { duration: '3m', target: 100 },  // Stay at 100 VUs for 3 minutes
    { duration: '1m', target: 0 },    // Ramp down to 0 VUs
  ],
  
  // Thresholds (pass/fail criteria)
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
    http_reqs: ['rate>100'],           // Throughput > 100 RPS
    iteration_duration: ['p(95)<2000'],
  },
  
  // Tags for filtering metrics
  tags: {
    test_type: 'load',
    environment: 'staging',
  },
};
```

---

## Load Patterns & Scenarios

### Ramp-Up Pattern

**Purpose**: Gradually increase load to find saturation point

**Pattern**:
```javascript
stages: [
  { duration: '2m', target: 50 },   // Ramp to 50 VUs
  { duration: '5m', target: 50 },   // Sustain 50 VUs
  { duration: '2m', target: 100 },  // Ramp to 100 VUs
  { duration: '5m', target: 100 },  // Sustain 100 VUs
  { duration: '2m', target: 150 }, // Ramp to 150 VUs
  { duration: '5m', target: 150 },  // Sustain 150 VUs
  { duration: '2m', target: 0 },    // Ramp down
]
```

**Use Case**: Finding maximum sustainable load

### Sustained Peak Pattern

**Purpose**: Test system stability under constant load

**Pattern**:
```javascript
stages: [
  { duration: '1m', target: 100 },  // Quick ramp-up
  { duration: '10m', target: 100 }, // Sustain for extended period
  { duration: '1m', target: 0 },    // Ramp down
]
```

**Use Case**: Testing for memory leaks, resource exhaustion

### Spike Pattern

**Purpose**: Test system response to sudden load increases

**Pattern**:
```javascript
stages: [
  { duration: '1m', target: 10 },   // Normal load
  { duration: '10s', target: 500 }, // Sudden spike
  { duration: '1m', target: 10 },    // Return to normal
]
```

**Use Case**: Testing resilience to traffic spikes (marketing campaigns, viral events)

### Step Pattern

**Purpose**: Test system at specific load levels

**Pattern**:
```javascript
stages: [
  { duration: '2m', target: 25 },   // Step 1: 25 VUs
  { duration: '2m', target: 50 },    // Step 2: 50 VUs
  { duration: '2m', target: 75 },   // Step 3: 75 VUs
  { duration: '2m', target: 100 },   // Step 4: 100 VUs
  { duration: '2m', target: 0 },    // Ramp down
]
```

**Use Case**: Testing specific load points, capacity planning

### Soak Testing Pattern

**Purpose**: Test system over extended period

**Pattern**:
```javascript
stages: [
  { duration: '5m', target: 50 },   // Ramp up
  { duration: '2h', target: 50 },    // Soak for 2 hours
  { duration: '5m', target: 0 },     // Ramp down
]
```

**Use Case**: Testing for memory leaks, resource exhaustion over time

### Custom Scenarios

**Multiple Scenarios**:
```javascript
export const options = {
  scenarios: {
    // Scenario 1: API load
    api_load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },
        { duration: '5m', target: 100 },
        { duration: '2m', target: 0 },
      ],
      gracefulRampDown: '30s',
    },
    // Scenario 2: Background jobs
    background_jobs: {
      executor: 'constant-vus',
      vus: 10,
      duration: '10m',
    },
  },
};
```

---

## Metrics & Monitoring

### Key Metrics to Monitor

#### Latency Metrics

**Response Time Distribution**:
- P50 (median): Typical user experience
- P95: User-visible pain threshold
- P99: System stress indicator
- P99.9: Extreme tail events
- Max: Worst-case scenarios

**k6 Metrics**:
- `http_req_duration`: Total request duration
- `http_req_waiting`: Time waiting for response
- `http_req_connecting`: Time establishing connection
- `http_req_sending`: Time sending request
- `http_req_receiving`: Time receiving response

#### Throughput Metrics

**Requests per Second (RPS)**:
- Overall RPS
- RPS by endpoint
- RPS trends over time

**k6 Metrics**:
- `http_reqs`: Total HTTP requests
- `iterations`: Total test iterations

#### Error Metrics

**Error Rates**:
- Overall error rate
- Error rate by endpoint
- Error rate by error type
- Error rate trends

**k6 Metrics**:
- `http_req_failed`: Failed request rate
- `checks`: Custom check failures

#### Resource Utilization

**System Metrics** (monitor on server side):
- CPU usage
- Memory usage
- Disk I/O
- Network I/O
- Database connections
- Thread pool utilization

### k6 Built-in Metrics

**HTTP Metrics**:
- `http_reqs`: Total requests
- `http_req_duration`: Request duration
- `http_req_failed`: Failed requests
- `http_req_waiting`: Waiting time
- `http_req_connecting`: Connection time
- `http_req_sending`: Sending time
- `http_req_receiving`: Receiving time

**VU Metrics**:
- `vus`: Current virtual users
- `vus_max`: Maximum virtual users
- `iterations`: Total iterations
- `iteration_duration`: Iteration duration

**Custom Metrics**:
```javascript
import { Trend, Counter, Rate, Gauge } from 'k6/metrics';

const customTrend = new Trend('custom_duration');
const customCounter = new Counter('custom_count');
const customRate = new Rate('custom_rate');
const customGauge = new Gauge('custom_value');

export default function () {
  customTrend.add(123);
  customCounter.add(1);
  customRate.add(1);
  customGauge.add(42);
}
```

### Thresholds & Pass/Fail Criteria

**Define Thresholds**:
```javascript
thresholds: {
  // Latency thresholds
  http_req_duration: [
    'p(50)<200',   // 50% of requests < 200ms
    'p(95)<500',   // 95% of requests < 500ms
    'p(99)<1000',  // 99% of requests < 1s
  ],
  
  // Error rate threshold
  http_req_failed: ['rate<0.01'],  // Error rate < 1%
  
  // Throughput threshold
  http_reqs: ['rate>100'],          // Throughput > 100 RPS
  
  // Custom metric thresholds
  custom_duration: ['p(95)<300'],
}
```

---

## Result Interpretation

### Understanding Results

#### Latency Analysis

**Key Patterns**:
- **Latency increases before errors**: System degrading gracefully
- **Sudden latency spikes**: Resource exhaustion, bottlenecks
- **Gradual latency increase**: Saturation approaching
- **Flat latency**: System handling load well

**Interpretation**:
- P95 latency increasing → System approaching limits
- P99 latency spiking → Resource contention
- Latency variance high → Unpredictable performance

#### Error Analysis

**Error Patterns**:
- **Gradual error increase**: Capacity limits reached
- **Sudden error spike**: System failure, resource exhaustion
- **Intermittent errors**: Resource contention, race conditions
- **Error rate correlates with latency**: System overload

**Error Types**:
- **5xx errors**: Server-side issues
- **4xx errors**: Client-side issues (may indicate test problems)
- **Timeouts**: System too slow, resource exhaustion
- **Connection errors**: Resource limits, network issues

#### Throughput Analysis

**Throughput Patterns**:
- **Throughput plateaus**: Maximum capacity reached
- **Throughput decreases**: System degrading
- **Throughput variance**: Unstable performance
- **Throughput correlates with errors**: System overload

#### Resource Correlation

**Correlate Metrics**:
- High latency + High CPU → CPU-bound bottleneck
- High latency + High I/O wait → I/O-bound bottleneck
- High latency + High memory → Memory pressure
- High latency + High connection count → Connection pool exhaustion

### Common Result Patterns

#### Pattern 1: Healthy System
- **Latency**: Stable, within thresholds
- **Errors**: Low, < 1%
- **Throughput**: Meets target
- **Resources**: Utilization < 80%
- **Interpretation**: System handling load well

#### Pattern 2: Approaching Limits
- **Latency**: Gradually increasing
- **Errors**: Slightly increasing
- **Throughput**: Plateauing
- **Resources**: Utilization 80-90%
- **Interpretation**: Near capacity, monitor closely

#### Pattern 3: System Overload
- **Latency**: Spiking, exceeding thresholds
- **Errors**: High, > 5%
- **Throughput**: Decreasing
- **Resources**: Utilization > 90%
- **Interpretation**: System overloaded, needs optimization

#### Pattern 4: Resource Exhaustion
- **Latency**: Sudden spikes
- **Errors**: Sudden increase
- **Throughput**: Sudden drop
- **Resources**: At 100% utilization
- **Interpretation**: Resource exhausted, system failure

---

## Production-Safe Testing

### Testing in Staging

**Best Practice**: Always test in staging first

**Requirements**:
- Staging environment matches production
- Same infrastructure and configuration
- Representative data volumes
- Isolated from production

### Testing in Production (Canary)

**When Appropriate**:
- Validating staging test results
- Testing production-specific configurations
- Gradual rollout validation

**Safety Measures**:
- **Canary deployment**: Small percentage of traffic
- **Feature flags**: Quick rollback capability
- **Monitoring**: Real-time metrics watching
- **Rollback plan**: Immediate reversion capability
- **Time windows**: Low-traffic periods
- **Gradual increase**: Start small, increase slowly

**k6 Canary Test Example**:
```javascript
export const options = {
  stages: [
    { duration: '1m', target: 1 },    // Start with 1 VU
    { duration: '2m', target: 5 },     // Gradually increase
    { duration: '2m', target: 10 },    // Continue gradual increase
    { duration: '1m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_failed: ['rate<0.001'],   // Very strict error threshold
  },
};
```

### Avoiding Production Impact

**Do's**:
- ✅ Test during low-traffic windows
- ✅ Use rate limiting to cap load
- ✅ Monitor production metrics closely
- ✅ Have rollback plan ready
- ✅ Test incrementally

**Don'ts**:
- ❌ Test during peak traffic
- ❌ Test without monitoring
- ❌ Test without rollback plan
- ❌ Test with unlimited load
- ❌ Test critical user flows in production

---

## Advanced Techniques

### Realistic User Behavior

**Think Time**:
```javascript
export default function () {
  http.get('https://api.example.com/products');
  sleep(Math.random() * 3 + 1);  // Random think time 1-4s
  
  http.get('https://api.example.com/cart');
  sleep(Math.random() * 2 + 0.5);  // Random think time 0.5-2.5s
}
```

**User Journeys**:
```javascript
export default function () {
  // Browse products
  http.get('https://api.example.com/products');
  sleep(2);
  
  // View product details
  const productId = '12345';
  http.get(`https://api.example.com/products/${productId}`);
  sleep(1);
  
  // Add to cart
  http.post('https://api.example.com/cart', JSON.stringify({
    productId: productId,
    quantity: 1,
  }));
  sleep(1);
  
  // Checkout
  http.post('https://api.example.com/checkout', JSON.stringify({
    cartId: 'cart-123',
  }));
}
```

### Data-Driven Testing

**CSV Data**:
```javascript
import { SharedArray } from 'k6/data';
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';

const data = new SharedArray('users', function () {
  return papaparse.parse(open('./users.csv'), { header: true }).data;
});

export default function () {
  const user = data[__VU % data.length];
  http.get(`https://api.example.com/users/${user.id}`);
}
```

### Custom Metrics & Checks

**Advanced Checks**:
```javascript
import { check } from 'k6';
import http from 'k6/http';

export default function () {
  const response = http.get('https://api.example.com/endpoint');
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'response has data': (r) => r.json().data !== null,
    'response size > 100 bytes': (r) => r.body.length > 100,
  });
}
```

### Distributed Testing

**k6 Cloud**:
- Run tests from multiple locations
- Scale beyond single machine limits
- Real-world network conditions

**k6 Operator (Kubernetes)**:
- Run tests in Kubernetes cluster
- Scale test execution
- Resource management

---

## Common Mistakes & Pitfalls

### Mistake 1: Testing from Localhost

**Problem**: Network conditions don't match production  
**Impact**: Inaccurate latency measurements  
**Solution**: Test from production-like network or use k6 Cloud

### Mistake 2: Ignoring Warm-Up

**Problem**: Cold start affects initial metrics  
**Impact**: Inaccurate baseline measurements  
**Solution**: Include warm-up period in test

**Example**:
```javascript
stages: [
  { duration: '1m', target: 10 },   // Warm-up
  { duration: '5m', target: 100 },  // Actual test
]
```

### Mistake 3: Comparing to Averages

**Problem**: Averages hide tail latency  
**Impact**: Missing user-visible performance issues  
**Solution**: Always use percentiles (P95, P99)

### Mistake 4: Testing Unrealistic Scenarios

**Problem**: Tests don't match real usage  
**Impact**: Results don't reflect production behavior  
**Solution**: Model real user behavior

### Mistake 5: No Baseline Comparison

**Problem**: Can't measure improvement  
**Impact**: Don't know if changes helped  
**Solution**: Always establish baseline before changes

### Mistake 6: Testing Everything at Once

**Problem**: Can't identify root cause  
**Impact**: Confounding variables  
**Solution**: Test one thing at a time

### Mistake 7: Ignoring Resource Metrics

**Problem**: Only looking at latency/errors  
**Impact**: Missing resource bottlenecks  
**Solution**: Monitor CPU, memory, I/O, connections

### Mistake 8: Not Testing Failure Scenarios

**Problem**: Don't know system limits  
**Impact**: Surprised by production failures  
**Solution**: Test beyond expected load

---

## Best Practices Summary

### Test Design
- ✅ Define clear objectives and hypotheses
- ✅ Test one thing at a time
- ✅ Use realistic user behavior
- ✅ Include warm-up periods
- ✅ Test incrementally (start small)

### Metrics & Monitoring
- ✅ Use percentiles, not averages
- ✅ Monitor latency, errors, throughput, resources
- ✅ Set appropriate thresholds
- ✅ Correlate metrics
- ✅ Document all metrics

### Safety
- ✅ Test in staging first
- ✅ Use canary deployments for production
- ✅ Monitor production metrics closely
- ✅ Have rollback plan ready
- ✅ Test during low-traffic windows

### Analysis
- ✅ Compare before/after
- ✅ Identify patterns and trends
- ✅ Correlate metrics
- ✅ Document findings
- ✅ Iterate based on results

---

## Next Steps

After conducting load tests:

1. **Analyze results**: Identify bottlenecks and patterns
2. **Document findings**: Record all metrics and observations
3. **Prioritize fixes**: Rank issues by impact
4. **Implement optimizations**: Apply fixes systematically
5. **Re-test**: Validate improvements with new tests
6. **Iterate**: Continue testing and optimizing
