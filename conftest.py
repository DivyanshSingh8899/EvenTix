import pytest
import sys
import os
from datetime import datetime, timezone

# Add the app directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db, User, Event, Booking
from config import TestConfig
from werkzeug.security import generate_password_hash


@pytest.fixture
def app_context():
    """Create application for testing"""
    app.config.from_object(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app_context):
    """Test client for the app"""
    return app_context.test_client()


@pytest.fixture
def runner(app_context):
    """Test CLI runner"""
    return app_context.test_cli_runner()


@pytest.fixture
def init_database(app_context):
    """Initialize database with test data"""
    # Create test users - check if admin exists first (created by app.py)
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@test.com',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
    
    regular_user = User(
        username='testuser',
        email='testuser@test.com',
        password=generate_password_hash('password123'),
        is_admin=False
    )
    
    db.session.add(regular_user)
    db.session.commit()
    
    # Create test events
    event1 = Event(
        title='Tech Conference 2026',
        description='Annual tech conference with industry leaders',
        date_time=datetime(2026, 5, 15, 10, 0),
        location='San Francisco, CA',
        total_tickets=100,
        available_tickets=100,
        ticket_price=99.99
    )
    
    event2 = Event(
        title='Web Development Workshop',
        description='Learn modern web development practices',
        date_time=datetime(2026, 4, 10, 14, 0),
        location='New York, NY',
        total_tickets=50,
        available_tickets=45,
        ticket_price=49.99
    )
    
    db.session.add(event1)
    db.session.add(event2)
    db.session.commit()
    
    # Create test booking
    booking = Booking(
        user_id=regular_user.id,
        event_id=event2.id,
        num_tickets=5,
        total_price=249.95
    )
    db.session.add(booking)
    db.session.commit()
    
    return {
        'admin_user': admin_user,
        'regular_user': regular_user,
        'event1': event1,
        'event2': event2,
        'booking': booking
    }


@pytest.fixture
def auth_headers(client, init_database):
    """Get authentication headers by logging in"""
    response = client.post(
        '/login',
        data={
            'username': 'testuser',
            'password': 'password123'
        }
    )
    return {'Referer': 'http://localhost/'}
