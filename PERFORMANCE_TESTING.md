# Performance Testing Guide

## Overview

Performance testing measures how well your Event Management System responds under various conditions:
- **Response Times** - How fast pages load
- **Throughput** - Requests handled per second
- **Concurrent Load** - Multiple users accessing simultaneously
- **Memory Usage** - RAM consumption during operation
- **Error Handling** - Performance under error conditions

## Performance Test Targets

| Metric | Target | Category |
|--------|--------|----------|
| Home Page Load | < 200ms | Response Time |
| Events Page Load | < 300ms | Response Time |
| Event Detail Load | < 150ms | Response Time |
| Admin Dashboard | < 500ms | Response Time |
| Login | < 200ms | Response Time |
| Booking | < 300ms | Response Time |
| QR Code Generation | < 100ms | Response Time |
| Concurrent Requests | 10+ req/sec | Throughput |
| Login Throughput | 5+ req/sec | Throughput |
| Response Size (Home) | < 2MB | Response Size |
| Response Size (Events) | < 3MB | Response Size |

---

## 🚀 Running Performance Tests

### Run All Performance Tests
```bash
pytest tests/test_performance.py -v
```

### Run Specific Performance Test
```bash
pytest tests/test_performance.py::TestResponseTimes -v
pytest tests/test_performance.py::TestConcurrentRequests -v
```

### Run with Detailed Output
```bash
pytest tests/test_performance.py -v -s
```

Shows execution times and throughput metrics.

### Run Specific Test Class
```bash
# Test response times
pytest tests/test_performance.py::TestResponseTimes -v

# Test concurrent requests
pytest tests/test_performance.py::TestConcurrentRequests -v

# Test throughput
pytest tests/test_performance.py::TestThroughput -v
```

---

## 📊 Performance Test Categories

### 1. TestResponseTimes (7 tests)
Tests individual page load times to ensure they meet performance targets.

**What it tests:**
- Home page responds in < 200ms
- Events listing in < 300ms
- Event details in < 150ms
- Admin dashboard in < 500ms
- Login in < 200ms
- Booking in < 300ms
- QR code generation in < 100ms

**Why it matters:**
- Slow pages frustrate users
- Each 100ms delay reduces conversions by 1%
- Mobile users need fast responses

**Run it:**
```bash
pytest tests/test_performance.py::TestResponseTimes -v -s
```

### 2. TestConcurrentRequests (2 tests)
Tests system behavior when multiple users access simultaneously.

**What it tests:**
- 10 concurrent home page requests
- 10 concurrent event listing requests

**Why it matters:**
- Real users don't access serially
- Peak traffic times have many simultaneous users
- System should handle concurrent load gracefully

**Run it:**
```bash
pytest tests/test_performance.py::TestConcurrentRequests -v -s
```

**Example output:**
```
10 concurrent requests - Avg: 250ms, Max: 350ms
```

### 3. TestThroughput (2 tests)
Measures requests per second the system can handle.

**What it tests:**
- Home page throughput: 50 requests
- Login throughput: 20 requests

**Why it matters:**
- Determines server capacity
- Helps plan infrastructure scaling
- Identifies bottlenecks

**Run it:**
```bash
pytest tests/test_performance.py::TestThroughput -v -s
```

**Example output:**
```
Home page throughput: 45.23 requests/sec
Login throughput: 12.5 requests/sec
```

### 4. TestMemoryUsage (1 test)
Monitors memory consumption during operations.

**What it tests:**
- Event listing pages don't leak memory
- Peak memory stays under 10MB

**Why it matters:**
- Memory leaks can crash servers
- Cloud hosting charged by memory
- Long-running servers need stable memory

**Run it:**
```bash
pytest tests/test_performance.py::TestMemoryUsage -v -s
```

### 5. TestResponseQuality (3 tests)
Ensures responses include all expected content.

**What it tests:**
- Home page completeness
- Events page content
- Admin dashboard statistics

**Why it matters:**
- Fast but incomplete responses are useless
- Must balance speed with functionality

### 6. TestErrorHandling (2 tests)
Tests performance under error conditions.

**What it tests:**
- 404 errors respond quickly
- Invalid bookings handled efficiently

**Why it matters:**
- Errors shouldn't crash or slow system
- Fast error responses improve UX

### 7. TestDatabasePerformance (2 tests)
Tests database query efficiency.

**What it tests:**
- Event queries complete in < 50ms
- User lookups in < 30ms

**Why it matters:**
- Database is often the bottleneck
- Slow queries cascade to slow responses
- Need proper indexing

### 8. TestResponseSizes (2 tests)
Ensures responses aren't unnecessarily large.

**What it tests:**
- Home page < 2MB
- Events page < 3MB

**Why it matters:**
- Large responses waste bandwidth
- Mobile users on slow connections
- CDN caching works better with smaller files

---

## 📈 Interpreting Results

### Passing Performance Test
```
tests/test_performance.py::TestResponseTimes::test_home_page_response_time PASSED [ 10%]
tests/test_performance.py::TestThroughput::test_home_page_throughput PASSED
Home page throughput: 45.23 requests/sec
```

✅ **What it means:** Your page is fast enough

### Failing Performance Test
```
FAILED tests/test_performance.py::TestResponseTimes::test_home_page_response_time
AssertionError: assert 250 < 200
Home page took 250ms (target: < 200ms)
```

⚠️ **What it means:** 
- Home page is 50ms slower than target
- Need to optimize to meet SLA

### Performance Test Output Example
```bash
$ pytest tests/test_performance.py -v -s

====================== test session starts ======================
...
TestResponseTimes::test_home_page_response_time PASSED          [ 10%]
TestResponseTimes::test_events_listing_response_time PASSED     [ 20%]
TestResponseTimes::test_event_detail_response_time PASSED       [ 30%]

TestConcurrentRequests::test_multiple_concurrent_home_requests
10 concurrent requests - Avg: 250ms, Max: 350ms
PASSED                                                          [ 40%]

TestThroughput::test_home_page_throughput
Home page throughput: 45.23 requests/sec
PASSED                                                          [ 50%]

TestMemoryUsage::test_event_listing_memory
Events page - Current: 1250.45KB, Peak: 3456.78KB
PASSED                                                          [ 60%]

====================== 20 passed in 45.23s ======================
```

---

## 🔧 Optimization Tips

### If Response Time is Too High

**1. Profile the Code**
```bash
# Add profiling to your tests
pip install py-spy
py-spy record -o profile.svg -- pytest tests/test_performance.py
```

**2. Check Database Queries**
- Add indexes to frequently queried columns
- Use `db.session.query(...).join(...)` for relationships
- Avoid N+1 query problems

**3. Cache Static Content**
```python
@app.route('/static/...')
@cache.cached(timeout=3600)
def static_file():
    ...
```

**4. Optimize Templates**
- Minimize loops
- Cache template fragments
- Use Jinja2 optimizations

### If Throughput is Low

**1. Increase Workers**
```bash
# Use gunicorn with multiple workers
gunicorn -w 4 --bind 0.0.0.0:5000 app:app
```

**2. Use Connection Pooling**
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 3600,
}
```

**3. Enable Caching**
```bash
pip install flask-caching
```

### If Memory Usage is High

**1. Find Memory Leaks**
```bash
pip install memory-profiler
python -m memory_profiler app.py
```

**2. Use Generators**
```python
# Instead of loading all at once
events = Event.query.all()  # BAD - loads all

# Use pagination
events = Event.query.paginate(page=1, per_page=20)  # GOOD
```

**3. Clear Session**
```python
db.session.expunge_all()  # Clear from memory
```

---

## 📊 Performance Baseline

### Current Performance (Baseline)
Document current performance to track improvements:

```
Test Date: 2026-03-30
Python Version: 3.13
Database: SQLite
Server: Flask Development Server

Home Page:           150ms  ✅
Events Page:         250ms  ✅
Event Detail:        120ms  ✅
Admin Dashboard:     400ms  ✅
Login:              180ms  ✅
Booking:            280ms  ✅
QR Code:             85ms  ✅

Concurrent (10 req): 250ms avg  ✅
Throughput:         45 req/sec  ✅

Peak Memory:        3.5MB  ✅
Home Page Size:     150KB  ✅
```

---

## 🎯 Performance vs. Features

**Trade-offs to Consider:**

| Optimization | Benefit | Cost |
|-------------|---------|------|
| Response Caching | Very fast responses | Stale data |
| Database Indexing | Faster queries | More disk space |
| Load Balancing | More capacity | Infrastructure cost |
| CDN | Faster global access | Service cost |
| Compression | Smaller responses | CPU usage |

---

## 📋 Performance Testing Checklist

When making changes to your code:

- [ ] Run performance tests: `pytest tests/test_performance.py`
- [ ] Check response times: All under target
- [ ] Verify throughput: Meets minimum requirement
- [ ] Monitor memory: No leaks detected
- [ ] Validate response content: Complete and correct
- [ ] Document changes: Note what was optimized
- [ ] Benchmark: Compare before/after

---

## 🔄 Continuous Performance Monitoring

### Add Performance Testing to CI/CD

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
      - run: pytest tests/test_performance.py -v --tb=short
```

### Track Performance Over Time

Create a performance tracking file:
```
performance-history.txt

Date       | Home  | Events | Booking | Throughput
-----------|-------|--------|---------|----------
2026-03-20 | 180ms | 280ms  | 300ms   | 42 req/sec
2026-03-25 | 170ms | 270ms  | 290ms   | 45 req/sec
2026-03-30 | 150ms | 250ms  | 280ms   | 48 req/sec
```

---

## 🚀 Performance Targets by Stage

### Development
- Fast feedback for developers
- Targets: 1-2 seconds per action

### Testing
- Realistic browser performance
- Targets: < 500ms per page
- Targets: 10+ concurrent users

### Production
- Real user expectations
- Targets: < 200ms per page
- Targets: Handles peak load
- Targets: 99.9% uptime

---

## 📚 Performance Testing Tools

### Built-in (Already Included)
- `pytest` - Test framework
- `time` module - Timing measurements
- `tracemalloc` - Memory tracking
- `ThreadPoolExecutor` - Concurrent load

### Recommended Additional Tools

**Apache Bench** - Simple HTTP load testing
```bash
ab -n 1000 -c 10 http://localhost:5000/
```

**Locust** - Load testing framework
```bash
# Install
pip install locust

# Run
locust -f locustfile.py
```

**wrk** - Modern HTTP benchmarking
```bash
wrk -t4 -c100 -d30s http://localhost:5000/
```

**py-spy** - Python profiling
```bash
pip install py-spy
py-spy record -o profile.svg -- pytest tests/test_performance.py
```

---

## ✅ Performance Testing Best Practices

1. **Test Early and Often** - Catch performance regressions early
2. **Test Realistic Scenarios** - Use actual user data patterns
3. **Monitor Consistently** - Track performance over time
4. **Isolate Variables** - Test one change at a time
5. **Use Baselines** - Compare against previous performance
6. **Test Under Load** - Don't just test single users
7. **Document Results** - Keep performance history
8. **Optimize Later** - Write correct code first, optimize later
9. **Profile First** - Use profilers to find real bottlenecks
10. **Think About UX** - Performance matters to users

---

## 🎓 Quick Commands

```bash
# Run all performance tests
pytest tests/test_performance.py -v

# Run specific category
pytest tests/test_performance.py::TestResponseTimes -v

# Show timing details
pytest tests/test_performance.py -v -s

# Continue on failures (to see all results)
pytest tests/test_performance.py -v --tb=no

# Full output with all times displayed
pytest tests/test_performance.py -v -s --tb=short
```

---

## 📞 Troubleshooting

**Tests are hanging:**
- Reduce concurrent requests
- Check for database locks
- Monitor system resources

**Memory tests fail:**
- Check for circular references
- Use `gc.collect()` to force garbage collection
- Profile with `memory_profiler`

**Timing is inconsistent:**
- Run tests multiple times
- Use statistical analysis
- Run on dedicated hardware

---

## Summary

Performance testing ensures your Event Management System:
- ✅ Loads fast for users
- ✅ Handles multiple users
- ✅ Uses memory efficiently
- ✅ Maintains quality under load
- ✅ Meets business SLAs

Start with `pytest tests/test_performance.py -v` to check your baseline performance!
