"""
Test cases for database models
"""
import pytest
from datetime import datetime
from app import db, User, Event, Booking
from werkzeug.security import check_password_hash, generate_password_hash


class TestUserModel:
    """Test User model"""
    
    def test_user_creation(self, app_context):
        """Test creating a user"""
        user = User(
            username='john_doe',
            email='john@example.com',
            password=generate_password_hash('password123'),
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == 'john_doe'
        assert user.email == 'john@example.com'
        assert user.is_admin is False
        assert check_password_hash(user.password, 'password123')
    
    def test_user_password_hashing(self, app_context):
        """Test password is properly hashed"""
        password = 'my_secure_password'
        user = User(
            username='secure_user',
            email='secure@example.com',
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        assert check_password_hash(user.password, password)
        assert user.password != password  # Password should be hashed
    
    def test_user_unique_username(self, app_context):
        """Test username must be unique"""
        user1 = User(
            username='duplicate',
            email='user1@example.com',
            password=generate_password_hash('pass1')
        )
        db.session.add(user1)
        db.session.commit()
        
        user2 = User(
            username='duplicate',
            email='user2@example.com',
            password=generate_password_hash('pass2')
        )
        db.session.add(user2)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()
    
    def test_user_unique_email(self, app_context):
        """Test email must be unique"""
        user1 = User(
            username='user1',
            email='duplicate@example.com',
            password=generate_password_hash('pass1')
        )
        db.session.add(user1)
        db.session.commit()
        
        user2 = User(
            username='user2',
            email='duplicate@example.com',
            password=generate_password_hash('pass2')
        )
        db.session.add(user2)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()


class TestEventModel:
    """Test Event model"""
    
    def test_event_creation(self, app_context):
        """Test creating an event"""
        event = Event(
            title='Web Summit 2026',
            description='The biggest web conference',
            date_time=datetime(2026, 6, 15),
            location='Las Vegas, NV',
            total_tickets=500,
            available_tickets=500,
            ticket_price=150.00
        )
        db.session.add(event)
        db.session.commit()
        
        assert event.id is not None
        assert event.title == 'Web Summit 2026'
        assert event.available_tickets == 500
        assert event.ticket_price == 150.00
    
    def test_event_ticket_availability(self, app_context):
        """Test ticket availability calculation"""
        event = Event(
            title='Test Event',
            description='Testing availability',
            date_time=datetime(2026, 5, 1),
            location='Test Location',
            total_tickets=100,
            available_tickets=100,
            ticket_price=50.00
        )
        db.session.add(event)
        db.session.commit()
        
        # Simulate ticket booking
        event.available_tickets -= 30
        db.session.commit()
        
        assert event.available_tickets == 70
        assert event.total_tickets == 100
    
    def test_event_sold_out(self, app_context):
        """Test sold out event"""
        event = Event(
            title='Limited Event',
            description='Limited tickets',
            date_time=datetime(2026, 4, 1),
            location='Test Location',
            total_tickets=10,
            available_tickets=0,
            ticket_price=25.00
        )
        db.session.add(event)
        db.session.commit()
        
        assert event.available_tickets == 0


class TestBookingModel:
    """Test Booking model"""
    
    def test_booking_creation(self, app_context, init_database):
        """Test creating a booking"""
        data = init_database
        
        booking = Booking(
            user_id=data['regular_user'].id,
            event_id=data['event1'].id,
            num_tickets=5,
            total_price=499.95
        )
        db.session.add(booking)
        db.session.commit()
        
        assert booking.id is not None
        assert booking.num_tickets == 5
        assert booking.total_price == 499.95
        assert booking.booking_reference is not None
    
    def test_booking_reference_unique(self, app_context, init_database):
        """Test booking reference is unique"""
        data = init_database
        
        booking1 = Booking(
            user_id=data['regular_user'].id,
            event_id=data['event1'].id,
            num_tickets=3,
            total_price=299.97
        )
        db.session.add(booking1)
        db.session.commit()
        
        assert len(booking1.booking_reference) == 36  
        assert booking1.booking_reference is not None
    
    def test_booking_relationships(self, app_context, init_database):
        """Test booking relationships with user and event"""
        data = init_database
        
        bookings = Booking.query.filter_by(user_id=data['regular_user'].id).all()
        
        assert len(bookings) > 0
        for booking in bookings:
            assert booking.user.username == 'testuser'
            assert booking.event is not None
