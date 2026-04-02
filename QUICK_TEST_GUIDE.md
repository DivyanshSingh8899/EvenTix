# Quick Test Command Reference

## Installation
```bash
pip install -r requirements-dev.txt
```

## Most Common Commands

### Run all tests
```bash
pytest
```

### Run with detailed output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/test_models.py
pytest tests/test_auth.py
```

### Run with coverage
```bash
pytest --cov
```

### Generate HTML coverage report
```bash
pytest --cov --cov-report=html
```

### Run tests and stop at first failure
```bash
pytest -x
```

### Run tests matching a pattern
```bash
pytest -k "test_login"
```

### Show print statements (remove output capture)
```bash
pytest -s
```

### Run specific test class
```bash
pytest tests/test_auth.py::TestAuthenticationRoutes
```

### Run specific test function
```bash
pytest tests/test_models.py::TestUserModel::test_user_creation
```

## Test Coverage Levels

- **100%** - Perfect (all code is tested)
- **80-99%** - Excellent (good coverage)
- **60-79%** - Good (most code tested)
- **< 60%** - Poor (significant gaps)

**Goal:** Aim for 80%+ code coverage

## Expected Test Results

✅ All ~40 test cases should PASS
Each test file has:
- **test_models.py**: ~9 tests
- **test_auth.py**: ~12 tests
- **test_events.py**: ~14 tests
- **test_admin.py**: ~11 tests

Total: ~46 tests

## Reading Test Output

### Success Format
```
===================== 46 passed in 2.34s =====================
```

### Failure Format
```
FAILED tests/test_auth.py::TestAuthenticationRoutes::test_login_success - AssertionError
```

## Continuous Integration

To run tests before commits:
```bash
pytest && git commit ...
```

## IDE Integration

### VS Code
1. Install "Python" extension
2. Install "Pytest" extension
3. Click on test file → "Run Test"

### PyCharm
- Right-click test file → "Run pytest"
- Click green play button next to test name
