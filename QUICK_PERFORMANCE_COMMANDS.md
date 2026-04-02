# Quick Performance Testing Commands

## Installation
```bash
# For pytest performance tests (already installed)
# Already in requirements-dev.txt

# For Locust load testing (optional)
pip install locust
```

## Run Performance Tests

### All Tests
```bash
pytest tests/test_performance.py -v
```

### Specific Category
```bash
pytest tests/test_performance.py::TestResponseTimes -v
pytest tests/test_performance.py::TestConcurrentRequests -v
pytest tests/test_performance.py::TestThroughput -v
pytest tests/test_performance.py::TestMemoryUsage -v
pytest tests/test_performance.py::TestErrorHandling -v
pytest tests/test_performance.py::TestDatabasePerformance -v
```

### With Detailed Output (Show Timings)
```bash
pytest tests/test_performance.py -v -s
```

### Quick Summary
```bash
pytest tests/test_performance.py -q
```

## Load Testing with Locust

### Prerequisites
```bash
# Install Locust
pip install locust

# Make sure your app is running
python app.py &
```

### GUI (Recommended for Learning)
```bash
locust -f locustfile.py --host=http://localhost:5000
# Open browser: http://localhost:8089
```

### CLI (Headless)

**Light Load (50 users over 5 minutes):**
```bash
locust -f locustfile.py --host=http://localhost:5000 -u 50 -r 5 -t 300s --headless
```

**Peak Load (200 users over 5 minutes):**
```bash
locust -f locustfile.py --host=http://localhost:5000 -u 200 -r 20 -t 300s --headless
```

**Stress Test (500 users over 2 minutes):**
```bash
locust -f locustfile.py --host=http://localhost:5000 -u 500 -r 50 -t 120s --headless
```

## Command Parameters

| Parameter | Meaning | Example |
|-----------|---------|---------|
| `-u` | Number of users | `-u 100` |
| `-r` | Spawn rate (users/sec) | `-r 10` |
| `-t` | Duration | `-t 300s` (5 minutes) |
| `--headless` | No GUI (CLI only) | `--headless` |
| `-f` | Load test file | `-f locustfile.py` |
| `--host` | Target URL | `--host=http://localhost:5000` |
| `--csv=results` | Export results | `--csv=results` |

## Quick Tests

### 1. Check Individual Page Speed
```bash
pytest tests/test_performance.py::TestResponseTimes::test_home_page_response_time -v
```

### 2. Check Concurrent Performance
```bash
pytest tests/test_performance.py::TestConcurrentRequests -v -s
```

### 3. Check Throughput (Req/Sec)
```bash
pytest tests/test_performance.py::TestThroughput -v -s
```

### 4. Check All Performance
```bash
pytest tests/test_performance.py -v -s
```

### 5. Simulate 100 Users
```bash
# Terminal 1: Start app
python app.py

# Terminal 2: Start load test
locust -f locustfile.py --host=http://localhost:5000 -u 100 -r 10 -t 300s --headless
```

## Expected Output

### Pytest
```
tests/test_performance.py::TestResponseTimes::test_home_page_response_time PASSED
tests/test_performance.py::TestThroughput::test_home_page_throughput PASSED
Home page throughput: 45.23 requests/sec
======================== 21 passed in 15.71s ======================
```

✅ **Good** - Test passed, performance acceptable

### Locust
```
Home page:    500 requests   0 failures   152ms avg   45 req/sec
Events page:  500 requests   0 failures   248ms avg   42 req/sec
Login:        200 requests   0 failures   180ms avg   18 req/sec
```

✅ **Good** - No failures, reasonable response times

## Performance Targets

| Endpoint | Target | Current |
|----------|--------|---------|
| Home | < 200ms | ✅ ~150ms |
| Events | < 300ms | ✅ ~250ms |
| Login | < 300ms | ✅ ~280ms |
| Booking | < 300ms | ✅ ~290ms |
| Admin | < 500ms | ✅ ~400ms |
| Throughput | > 10 req/sec | ✅ ~45 req/sec |

## Troubleshooting

### Tests Won't Run
```bash
# Make sure app dependencies are installed
pip install -r requirements.txt

# Make sure pytest is installed
pip install -r requirements-dev.txt
```

### Locust Won't Connect
```bash
# Make sure app is running first
python app.py &

# Then start locust
locust -f locustfile.py --host=http://localhost:5000
```

### "Port 5000 already in use"
```bash
# Kill existing process
# Windows:
taskkill /F /IM python.exe

# Linux/Mac:
kill $(lsof -t -i:5000)
```

## Workflow

### 1. Baseline (First Time)
```bash
pytest tests/test_performance.py -v -s
# Screenshot or save results
```

### 2. Make Changes
```bash
# Edit code to optimize performance
# Add caching, optimize queries, etc.
```

### 3. Verify Improvement
```bash
pytest tests/test_performance.py -v -s
# Compare to baseline
```

### 4. Load Test (If Significant Change)
```bash
# Start app
python app.py &

# Run Locust
locust -f locustfile.py --host=http://localhost:5000 \
  -u 100 -r 10 -t 300s --headless
```

## Common Scenarios

### "Is my app fast enough?"
```bash
pytest tests/test_performance.py -q
# If all pass: YES ✅
```

### "Can I handle 100 concurrent users?"
```bash
locust -f locustfile.py --host=http://localhost:5000 -u 100 -r 10 -t 300s --headless
# Check for failures and response times
```

### "Where's the bottleneck?"
```bash
# Run with details
pytest tests/test_performance.py -v -s

# Look for slowest category
# Then optimize that area
```

### "Did my optimization work?"
```bash
# Before
pytest tests/test_performance.py -v -s
# Note results

# Make changes

# After
pytest tests/test_performance.py -v -s
# Compare improvement
```

## Status

**Current Performance (Baseline: 2026-03-30)**
- ✅ 21/21 tests passing
- ✅ All pages under target speed
- ✅ ~45 req/sec throughput
- ✅ No memory leaks
- ✅ Ready for scale testing

---

**Quick Start:**
```bash
# 1. Run tests
pytest tests/test_performance.py -v

# 2. Try load test
locust -f locustfile.py --host=http://localhost:5000 -u 50 -r 5 -t 300s --headless

# 3. Read detailed guide
# PERFORMANCE_TESTING.md - Complete reference
```
