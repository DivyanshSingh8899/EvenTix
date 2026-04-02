# Event Booking System - Testing Guide

## Overview
This guide explains how to perform testing for the Event Management System modules.

## Testing Tools & Frameworks
- **pytest**: Main testing framework
- **pytest-cov**: Code coverage reporting
- **pytest-flask**: Flask integration for pytest

## Installation

### 1. Install Testing Dependencies
```bash
pip install -r requirements-dev.txt
```

Or individually:
```bash
pip install pytest pytest-cov pytest-flask
```

## Test Structure

```
event-booking-system/
├── tests/
│   ├── __init__.py
│   ├── test_models.py          # Database model tests
│   ├── test_auth.py            # Authentication & Login/Register tests
│   ├── test_events.py          # Event browsing & booking tests
│   └── test_admin.py           # Admin dashboard & management tests
├── conftest.py                 # Pytest fixtures & configuration
├── config.py                   # Test configuration
└── app.py
```

## Running Tests

### 1. Run All Tests
```bash
pytest
```

### 2. Run Specific Test File
```bash
pytest tests/test_models.py
pytest tests/test_auth.py
pytest tests/test_events.py
pytest tests/test_admin.py
```

### 3. Run Specific Test Class
```bash
pytest tests/test_auth.py::TestAuthenticationRoutes
pytest tests/test_models.py::TestUserModel
```

### 4. Run Specific Test Function
```bash
pytest tests/test_auth.py::TestAuthenticationRoutes::test_login_success
pytest tests/test_models.py::TestUserModel::test_user_creation
```

### 5. Run with Verbose Output
```bash
pytest -v
```

### 6. Run with Print Statements
```bash
pytest -s
```

### 7. Generate Coverage Report
```bash
pytest --cov=. --cov-report=html
```
This creates an HTML coverage report in `htmlcov/index.html`

### 8. Show Coverage Summary
```bash
pytest --cov=. --cov-report=term-missing
```

## Test Modules Explained

### test_models.py
Tests database models and their functionality:
- **TestUserModel**: User creation, password hashing, uniqueness constraints
- **TestEventModel**: Event creation, ticket availability tracking
- **TestBookingModel**: Booking creation, relationships, references

**Key Tests:**
- `test_user_creation` - Verify user is created with correct attributes
- `test_user_password_hashing` - Ensure passwords are properly hashed
- `test_user_unique_username` - Verify duplicate usernames are rejected
- `test_event_ticket_availability` - Check ticket count updates
- `test_booking_creation` - Verify booking records are created correctly

### test_auth.py
Tests authentication and authorization:
- **TestAuthenticationRoutes**: Login, register, logout functionality

**Key Tests:**
- `test_register_new_user_success` - Register new user successfully
- `test_register_duplicate_username` - Reject duplicate usernames
- `test_login_success` - Login with correct credentials
- `test_login_wrong_password` - Reject invalid password
- `test_logout` - Verify logout functionality
- `test_admin_login` - Admin can login and access dashboard

### test_events.py
Tests event browsing and booking:
- **TestEventRoutes**: Event listing and detail pages
- **TestBookingRoutes**: Booking functionality and validation
- **TestQRCodeRoute**: QR code generation for bookings

**Key Tests:**
- `test_events_listing_page` - Events page loads correctly
- `test_event_detail_page` - Event detail page shows correct info
- `test_create_booking` - Create booking successfully
- `test_booking_exceeds_available_tickets` - Reject overbooking
- `test_qr_code_generation` - Generate QR code for booking

### test_admin.py
Tests admin dashboard and event management:
- **TestAdminRoutes**: Admin access control
- **TestAdminEventManagement**: Create, edit, delete events
- **TestAdminDashboardDisplay**: Dashboard information display

**Key Tests:**
- `test_admin_dashboard_requires_admin_privilege` - Only admins access dashboard
- `test_create_event_as_admin` - Admin can create events
- `test_edit_event_as_admin` - Admin can modify events
- `test_delete_event_as_admin` - Admin can delete events

## Fixtures (conftest.py)

### app_context
Provides Flask application context with test configuration and empty database

### client
Test client for making HTTP requests to the application

### runner
CLI runner for Flask CLI commands

### init_database
Initializes database with test data:
- **Users**: admin (is_admin=True), testuser (is_admin=False)
- **Events**: 2 sample events
- **Bookings**: 1 booking for testuser

Usage:
```python
def test_something(client, init_database):
    data = init_database
    admin = data['admin_user']
    event = data['event1']
    # ... test code
```

## Sample Test Execution

### Example 1: Run all authentication tests
```bash
pytest tests/test_auth.py -v
```

### Example 2: Run specific test with output
```bash
pytest tests/test_models.py::TestUserModel::test_user_creation -v -s
```

### Example 3: Generate coverage report
```bash
pytest --cov . --cov-report=html
# Then open htmlcov/index.html in browser
```

## Writing New Tests

### Template
```python
def test_feature_name(client, init_database):
    """Description of what this test does"""
    # Arrange - Set up test data
    data = init_database
    
    # Act - Perform the test action
    response = client.get('/some/route')
    
    # Assert - Check the results
    assert response.status_code == 200
    assert b'expected text' in response.data
```

### Best Practices
1. Use descriptive test names starting with `test_`
2. Use assertion messages for clarity: `assert condition, "message"`
3. Test one thing per test function
4. Use fixtures for common setup
5. Mock external dependencies
6. Test edge cases and error conditions

## Common Testing Scenarios

### 1. Test Protected Routes
```python
def test_route_requires_login(client):
    response = client.get('/admin')
    assert response.status_code == 302  # Redirect to login
```

### 2. Test Authentication Flow
```python
def test_login_flow(client, init_database):
    # Login
    response = client.post('/login', data={'username': 'admin', 'password': 'admin123'})
    assert response.status_code == 302
    
    # Access protected page
    response = client.get('/admin')
    assert response.status_code == 200
```

### 3. Test Form Submission
```python
def test_form_submit(client, init_database):
    response = client.post('/admin/event/new', data={
        'title': 'Event',
        'description': 'Desc',
        'date_time': '2026-06-01T10:00',
        'location': 'Location',
        'total_tickets': 100,
        'ticket_price': 50.00
    }, follow_redirects=True)
    assert response.status_code == 200
```

### 4. Test Database Relationships
```python
def test_booking_relationships(app_context, init_database):
    data = init_database
    booking = data['booking']
    
    assert booking.user.username == 'testuser'
    assert booking.event.title == 'Web Development Workshop'
```

## Interpreting Results

### Passed Test
```
tests/test_models.py::TestUserModel::test_user_creation PASSED
```

### Failed Test
```
tests/test_auth.py::TestAuthenticationRoutes::test_login_success FAILED
AssertionError: assert 302 == 200
```

### Coverage Report
```
Name                          Stmts   Miss  Cover
app.py                          150     5    96%
tests/__init__.py                0     0   100%
conftest.py                     45     0   100%
TOTAL                          195     5    97%
```

## Troubleshooting

### Issue: Tests fail with "Module not found"
**Solution:** Make sure you're in the project directory and fixtures import the app correctly

### Issue: Database errors in tests
**Solution:** Tests use in-memory SQLite (`:memory:`). Ensure conftest.py is in root directory

### Issue: Session/login not persisting
**Solution:** Use `follow_redirects=True` in client requests to follow redirects

### Issue: Tests passing locally but might fail in CI
**Solution:** Ensure test data (init_database) is independent and doesn't affect other tests

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov . --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## Performance Testing

### Run tests and show slowest 10
```bash
pytest --durations=10
```

## Next Steps

1. Install dev dependencies: `pip install -r requirements-dev.txt`
2. Run all tests: `pytest`
3. Create coverage report: `pytest --cov . --cov-report=html`
4. Write tests for new features before implementing them (TDD)
5. Maintain > 80% code coverage

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/testing/)
- [pytest-flask Documentation](https://pytest-flask.readthedocs.io/)
