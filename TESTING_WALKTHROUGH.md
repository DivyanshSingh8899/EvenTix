# Step-by-Step Testing Guide

## Installation (One-Time Setup)

### Step 1: Navigate to Project Directory
```bash
cd d:\Hackathon\Event_Management_System\event-booking-system
```

### Step 2: Activate Virtual Environment
```bash
# For Windows PowerShell
venv2\Scripts\Activate.ps1

# For Windows CMD
venv2\Scripts\activate.bat
```

### Step 3: Install Testing Dependencies
```bash
pip install pytest pytest-cov pytest-flask
```

Or install from file:
```bash
pip install -r requirements-dev.txt
```

**Expected Output:**
```
Successfully installed pytest-9.0.2 pytest-cov-7.1.0 pytest-flask-1.3.0
```

---

## Running Tests

### Basic: Run All Tests
```bash
pytest
```

**Output:**
```
======================== 50 passed in 34.62s ========================
```

---

### Verbose: See Individual Test Results
```bash
pytest -v
```

**Output Shows:**
```
tests/test_models.py::TestUserModel::test_user_creation PASSED     [ 82%]
tests/test_models.py::TestUserModel::test_user_password_hashing PASSED [ 84%]
tests/test_auth.py::TestAuthenticationRoutes::test_login_success PASSED [ 36%]
...
======================== 50 passed ========================
```

---

### Specific File: Run Tests from One Module
```bash
pytest tests/test_models.py -v
```

**Output:**
```
tests/test_models.py::TestUserModel::test_user_creation PASSED
tests/test_models.py::TestUserModel::test_user_password_hashing PASSED
tests/test_models.py::TestUserModel::test_user_unique_username PASSED
...
======================== 10 passed ========================
```

---

### Specific Class: Run Tests from One Test Class
```bash
pytest tests/test_auth.py::TestAuthenticationRoutes -v
```

**Output:**
```
test_register_page_accessible PASSED
test_register_new_user_success PASSED
test_register_duplicate_username PASSED
test_login_success PASSED
...
======================== 12 passed ========================
```

---

### Specific Test: Run Single Test Function
```bash
pytest tests/test_auth.py::TestAuthenticationRoutes::test_login_success -v
```

**Output:**
```
test_login_success PASSED [ 36%]
======================== 1 passed ========================
```

---

### With Print Output: See Console Output from Tests
```bash
pytest -s
```

**Use this to see print statements in test code**

---

### Stop on First Failure: Debug Failing Tests
```bash
pytest -x
```

**Stops execution at first failure**

---

### Show Slowest Tests: Performance Analysis
```bash
pytest --durations=5
```

**Output:**
```
slowest 5 durations
1.25s tests/test_admin.py::TestAdminEventManagement::test_create_event_as_admin
1.12s tests/test_admin.py::TestAdminEventManagement::test_edit_event_as_admin
0.95s tests/test_events.py::TestEventRoutes::test_events_listing_page
...
```

---

## Code Coverage Analysis

### Generate Coverage Report
```bash
pytest --cov . --cov-report=html
```

**Creates:** `htmlcov/index.html` - Detailed coverage report

**Output:**
```
Name              Stmts   Miss  Cover
app.py              150     5    96%
tests/conftest.py    45     0   100%
TOTAL              195     5    97%

htmlcov/index.html generated
```

### View Coverage Summary
```bash
pytest --cov . --cov-report=term-missing
```

**Output Shows Missing Lines**

---

## Filtering Tests

### Run Tests Matching a Pattern
```bash
pytest -k "login"
```

**Runs only tests with "login" in the name**

```bash
pytest -k "test_login"
pytest -k "auth"
pytest -k "admin"
```

---

## Practical Examples

### Example 1: Test User Authentication
```bash
cd d:\Hackathon\Event_Management_System\event-booking-system
venv2\Scripts\activate.bat
pytest tests/test_auth.py -v
```

**Expected:** 12 tests pass

---

### Example 2: Test Database Models
```bash
pytest tests/test_models.py -v -s
```

**Expected:** 10 tests pass with output

---

### Example 3: Test Event Booking Flow
```bash
pytest tests/test_events.py::TestBookingRoutes -v
```

**Expected:** 6 booking tests pass

---

### Example 4: Complete Coverage Report
```bash
pytest --cov . --cov-report=html
# Open htmlcov/index.html in browser
```

---

## Troubleshooting

### Issue: "pytest: command not found"
**Solution:** Install pytest
```bash
pip install pytest
```

### Issue: "No such file or directory"
**Solution:** Ensure you're in correct directory
```bash
cd d:\Hackathon\Event_Management_System\event-booking-system
```

### Issue: "Database is locked"
**Solution:** Close other instances or restart terminal

### Issue: Tests fail with import errors
**Solution:** Install app dependencies
```bash
pip install -r requirements.txt
```

---

## Complete Workflow

```bash
# 1. Navigate to project
cd d:\Hackathon\Event_Management_System\event-booking-system

# 2. Activate environment
venv2\Scripts\activate.bat

# 3. Install dev dependencies (first time only)
pip install -r requirements-dev.txt

# 4. Run tests
pytest

# 5. View coverage
pytest --cov --cov-report=html

# 6. Open coverage report (view results)
htmlcov\index.html
```

---

## Test Commands Summary Table

| Command | What it Does | Time |
|---------|-------------|------|
| `pytest` | Run all tests | ~35s |
| `pytest -v` | Show each test | ~35s |
| `pytest -x` | Stop at first failure | varies |
| `pytest -k login` | Only login tests | ~5s |
| `pytest --cov` | Show coverage | ~35s |
| `pytest tests/test_models.py` | Only model tests | ~8s |
| `pytest --durations=5` | Show slowest tests | ~35s |

---

## Success Indicators

✅ All tests should show **PASSED**
```
======================== 50 passed ========================
```

✅ No failures or errors

✅ Coverage should be **> 80%**

---

## Next: Continuous Testing

Add to development workflow:
```bash
# Before committing code
pytest && git commit -m "Feature: Add new functionality"

# Or use pre-commit hooks
# See: https://pre-commit.com/
```

---

## Need Help?

1. **Error in test:** Look at output, check test file
2. **Import errors:** Install requirements.txt
3. **Database errors:** Clear `database.db` if exists
4. **Performance:** Run `pytest --durations=10`

---

**You're all set! Start testing! 🚀**
