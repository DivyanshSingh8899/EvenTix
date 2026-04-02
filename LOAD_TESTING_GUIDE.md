# Load Testing & Performance Tools Guide

## 🎯 Performance Testing Pyramid

```
           ▲
          /│\
         / │ \  Load Testing (500+ users)
        /  │  \
       /   │   \
      /    │    \  Stress Testing (100+ users)
     /     │     \
    /      │      \
   /       │       \ Performance Tests (unit level)
  /        │        \
 ───────────────────── 
```

---

## 🔧 Performance Testing Tools

### 1. **pytest** (Unit Performers)
Already installed - tests individual endpoint performance.

```bash
pytest tests/test_performance.py -v
```

**Use for:** Response time baselines, quick checks

---

### 2. **Locust** (Load Testing)
Simulate real user behavior with concurrent load.

#### Installation
```bash
pip install locust
```

#### Running Load Tests

**Start Locust Web UI:**
```bash
locust -f locustfile.py --host=http://localhost:5000
```

Then open: `http://localhost:8089`

**Start Locust CLI (Headless):**
```bash
locust -f locustfile.py --host=http://localhost:5000 -u 100 -r 10 -t 60s
```

**Parameters:**
- `-u 100` - Number of users to simulate
- `-r 10` - Spawn rate (users per second)
- `-t 60s` - Duration (60 seconds)
- `--headless` - No GUI
- `--csv=results` - Export CSV results

#### Example Scenarios

**1. Ramp Up Test (gradual increase)**
```bash
locust -f locustfile.py --host=http://localhost:5000 -u 100 -r 5 -t 300s
```
Simulates 100 users joining over 20 seconds, runs for 5 minutes

**2. Peak Load Test (sudden spike)**
```bash
locust -f locustfile.py --host=http://localhost:5000 -u 500 -r 50 -t 120s
```
Simulates 500 users joining rapidly, runs for 2 minutes

**3. Sustained Load Test (long duration)**
```bash
locust -f locustfile.py --host=http://localhost:5000 -u 50 -r 5 -t 3600s
```
Simulates 50 users for 1 hour

#### Locust Metrics

After running, you'll see:

```
Requests    Failures    Avg (ms)    Min (ms)    Max (ms)    Rate
HOME        0           150         120         200         45/sec
EVENTS      0           250         200         350         50/sec
EVENT       0           120         100         180         40/sec
LOGIN       0           180         150         250         30/sec
BOOKING     0           280         240         400         20/sec

Response times:
- 50%ile (median): 200ms
- 95%ile: 350ms
- 99%ile: 500ms

Failures: 0
```

---

### 3. **Apache Bench** (Simple HTTP Load)
Simple command-line tool for basic load testing.

#### Installation (Windows)
```bash
# Using chocolatey
choco install apache

# Or download from Apache website
```

#### Running Tests

**Simple Load Test:**
```bash
ab -n 1000 -c 10 http://localhost:5000/
```

**Parameters:**
- `-n 1000` - Total requests
- `-c 10` - Concurrent connections
- `-t 60` - Timeout in seconds
- `-p data.json` - POST data file

**Example Output:**
```
Benchmarking localhost (be patient)...
Completed 100 requests
Completed 200 requests
...

Server Software:        Werkzeug/3.0.0
Server Hostname:        localhost
Server Port:            5000

Document Path:          /
Document Length:        5234 bytes

Concurrency Level:      10
Time taken for tests:   22.356 seconds
Complete requests:      1000
Failed requests:        0
Requests per second:    44.73 [#/sec]
Time per request:       223.56 [ms]
Time per request:       22.36 [ms] (mean, across all concurrent requests)
Transfer rate:          233.85 [Kbytes/sec]
```

---

### 4. **wrk** (Modern HTTP Benchmarking)

#### Installation (Windows via Chocolatey)
```bash
choco install wrk
```

#### Running Tests

```bash
# 4 threads, 100 connections, 30 seconds
wrk -t4 -c100 -d30s http://localhost:5000/

# With custom script
wrk -t4 -c100 -d30s -s script.lua http://localhost:5000/
```

**Parameters:**
- `-t4` - Number of threads
- `-c100` - Connections
- `-d30s` - Duration
- `-s script.lua` - Lua script for custom behavior

**Example Output:**
```
Running 30s test @ http://localhost:5000/
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   223.45ms  145.23ms   1.50s    78.34%
    Req/Sec    44.56     12.34    125.00     68.92%
  Latency Distribution
     50%   200.00ms
     75%   350.00ms
     90%   450.00ms
     99%   800.00ms
  5341 requests in 30.00s, 25.34MB read
Requests/sec:  178.03
Transfer/sec:  844.67KB
```

---

## 📊 Complete Performance Testing Workflow

### Step 1: Unit Performance Tests
```bash
# Verify individual endpoints meet performance targets
pytest tests/test_performance.py -v
```

### Step 2: Load Testing
```bash
# First: Make sure app is running
python app.py &

# Then: Start load test
locust -f locustfile.py --host=http://localhost:5000

# Or CLI:
locust -f locustfile.py --host=http://localhost:5000 -u 50 -r 5 -t 300s --headless
```

### Step 3: Analyze Results
- Check response times
- Identify bottlenecks
- Find breaking points

### Step 4: Optimize
- Cache frequently accessed data
- Optimize database queries
- Add indexes
- Scale infrastructure

### Step 5: Re-test
- Verify improvements
- Document changes
- Update baselines

---

## 🎯 Performance Testing Scenarios

### Scenario 1: Normal Traffic
**Goal:** Verify system handles typical workload

```bash
locust -f locustfile.py --host=http://localhost:5000 -u 50 -r 5 -t 300s
```

**Expected:**
- Response times < 300ms
- 0% failure rate
- System stable

### Scenario 2: Peak Traffic
**Goal:** Test system at maximum expected load

```bash
locust -f locustfile.py --host=http://localhost:5000 -u 200 -r 20 -t 300s
```

**Expected:**
- Response times < 500ms
- < 1% failure rate
- CPU/Memory reasonable

### Scenario 3: Stress Testing
**Goal:** Find system breaking point

```bash
locust -f locustfile.py --host=http://localhost:5000 -u 500 -r 50 -t 120s
```

**Expected:**
- System recovers after spike
- Graceful degradation
- No data corruption

### Scenario 4: Sustained Load
**Goal:** Detect memory leaks during long run

```bash
locust -f locustfile.py --host=http://localhost:5000 -u 100 -r 10 -t 3600s
```

**Expected:**
- Memory stays stable
- No performance degradation
- Handles connection cycles

---

## 📈 Understanding Percentiles

When you see response time percentiles:

```
50%ile (P50):  200ms  - Half requests answered in 200ms
95%ile (P95):  400ms  - 95% answered within 400ms
99%ile (P99):  600ms  - 99% answered within 600ms
```

**Good Targets:**
- P50: < 200ms (average user)
- P95: < 400ms (slower users)
- P99: < 800ms (slowest 1%)

---

## 🔍 Interpreting Performance Reports

### Red Flags 🚩
- Response times increasing over time (memory leak?)
- Errors increasing (system overload?)
- Response times vary wildly (contention?)
- Memory growing continuously (leak!)

### Green Lights 🟢
- Consistent response times
- 0% error rate
- Linear throughput scaling
- Stable memory usage

---

## 💡 Performance Optimization Tips

### Quick Wins
1. **Enable Caching**
   ```bash
   pip install flask-caching
   ```

2. **Add Database Indexes**
   ```python
   db.Index('idx_event_date', Event.date_time).create()
   ```

3. **Use Pagination**
   ```python
   events = Event.query.paginate(page=1, per_page=20)
   ```

4. **Compress Responses**
   ```bash
   pip install flask-compress
   ```

### Medium Effort
1. Asynchronous tasks (Celery)
2. Read replicas for database
3. CDN for static content
4. Query optimization

### Major Changes
1. Microservices architecture
2. Database sharding
3. Load balancing
4. Horizontal scaling

---

## 📊 Creating Performance Benchmarks

### Document Your Baseline
```
# performance_baseline.txt

Date: 2026-03-30
Environment: Flask dev server, SQLite, Single server
Load: Locust 50 users

Home Page:
  Average: 150ms
  95%ile:  300ms
  99%ile:  400ms

Events Page:
  Average: 250ms
  95%ile:  450ms
  99%ile:  600ms

System:
  Throughput: 44.73 req/sec
  Peak memory: 156MB
  Failures: 0%
```

### Track Progress
Update monthly and compare:
```
Metric              2026-03  2026-04  2026-05  Improvement
Home (avg):         150ms    140ms    130ms    13% ↓
Events (avg):       250ms    220ms    200ms    20% ↓
Throughput:         45/sec   48/sec   52/sec   15% ↑
Memory peak:        156MB    150MB    145MB    7% ↓
```

---

## 🚀 CI/CD Integration

### GitHub Actions Example
```yaml
name: Performance Tests
on: [push]
jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements-dev.txt
      - run: python app.py &
      - run: sleep 2
      - run: pytest tests/test_performance.py -v --tb=short
```

---

## 📋 Quick Command Reference

| Command | Purpose |
|---------|---------|
| `pytest tests/test_performance.py` | Unit performance tests |
| `locust -f locustfile.py --host=http://localhost:5000` | GUI load test |
| `locust -f locustfile.py -u 100 -r 10 -t 300s --headless` | Headless load test |
| `ab -n 1000 -c 10 http://localhost:5000/` | Apache Bench load test |
| `wrk -t4 -c100 -d30s http://localhost:5000/` | wrk benchmarking |

---

## ❓ FAQ

**Q: Should I run load tests while developing?**
A: No - develop first, optimize later. Write correct code, then optimize based on data.

**Q: How many users should I test with?**
A: Start with your average load, then test 2-3x that, then find breaking point.

**Q: Are pytest performance tests enough?**
A: Good for catching regressions. Load tests needed for realistic scenarios.

**Q: What's a good throughput target?**
A: Depends on your traffic. Typically 20-50 req/sec for small apps.

**Q: How often should I performance test?**
A: After major changes, before each release, monthly baseline.

---

## 📚 Resources

- [Locust Documentation](https://docs.locust.io/)
- [Apache Bench Documentation](https://httpd.apache.org/docs/2.4/programs/ab.html)
- [wrk GitHub](https://github.com/wg/wrk)
- [Performance Testing Best Practices](https://www.softwaretestinghelp.com/performance-testing/)

---

**Start with pytest tests, graduate to Locust for serious load testing! 🚀**
