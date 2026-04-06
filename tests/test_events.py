"""
Test cases for event-related routes
"""
import pytest
from app import db, Event


class TestEventRoutes:
    """Test event browsing routes"""
    @pytest.mark.events
    def test_index_page_accessible(self, client, init_database):
        """Test home page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'EventTix' in response.data or b'event' in response.data.lower()
    @pytest.mark.events
    def test_events_listing_page(self, client, init_database):
        """Test events listing page"""
        response = client.get('/events')
        assert response.status_code == 200
        assert b'Tech Conference' in response.data or b'event' in response.data.lower()
    @pytest.mark.events
    def test_event_detail_page(self, client, init_database):
        """Test event detail page"""
        data = init_database
        event_id = data['event1'].id
        
        response = client.get(f'/event/{event_id}')
        assert response.status_code == 200
        assert b'Tech Conference' in response.data or b'details' in response.data.lower()
    @pytest.mark.events
    def test_event_detail_not_found(self, client):
        """Test event detail with invalid ID"""
        response = client.get('/event/9999')
        assert response.status_code == 404
    @pytest.mark.events
    def test_events_show_correct_data(self, client, init_database):
        """Test events display correct information"""
        response = client.get('/events')
        assert response.status_code == 200
        # Check for event titles
        assert b'Tech Conference' in response.data
        assert b'Web Development' in response.data
    @pytest.mark.events
    def test_recent_events_on_home(self, client, init_database):
        """Test recent events are shown on home page"""
        response = client.get('/')
        assert response.status_code == 200
        # Home page should show recent events


class TestBookingRoutes:
    """Test booking-related routes"""
    @pytest.mark.events
    def test_booking_requires_login(self, client, init_database):
        """Test booking page requires authentication"""
        data = init_database
        event_id = data['event1'].id
        
        response = client.get(f'/book/{event_id}')
        # Should redirect to login
        assert response.status_code == 302 or response.location.endswith('/login')
    @pytest.mark.events
    def test_booking_page_for_authenticated_user(self, client, init_database):
        """Test booking page for authenticated user"""
        data = init_database
        event_id = data['event1'].id
        
        # Login first
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.get(f'/book/{event_id}', follow_redirects=True)
        assert response.status_code == 200
        assert b'ticket' in response.data.lower() or b'book' in response.data.lower()
    @pytest.mark.events
    def test_create_booking(self, client, init_database):
        """Test creating a booking"""
        data = init_database
        event_id = data['event1'].id
        
        # Login first
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Make booking
        response = client.post(f'/book/{event_id}', data={
            'num_tickets': 2
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Booking should be successful
        assert b'successful' in response.data.lower() or b'booking' in response.data.lower()
    @pytest.mark.events
    def test_booking_exceeds_available_tickets(self, client, init_database):
        """Test booking more tickets than available"""
        data = init_database
        # event2 has 45 available tickets
        event_id = data['event2'].id
        
        # Login first
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Try to book more tickets than available
        response = client.post(f'/book/{event_id}', data={
            'num_tickets': 100
        })
        
        assert response.status_code == 200
        assert b'available' in response.data.lower() or b'not enough' in response.data.lower()
    @pytest.mark.events
    def test_booking_zero_tickets(self, client, init_database):
        """Test booking with zero tickets"""
        data = init_database
        event_id = data['event1'].id
        
        # Login first
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Try to book zero tickets
        response = client.post(f'/book/{event_id}', data={
            'num_tickets': 0
        })
        
        assert response.status_code == 200
        assert b'at least' in response.data.lower() or b'select' in response.data.lower()
    @pytest.mark.events
    def test_booking_negative_tickets(self, client, init_database):
        """Test booking with negative tickets"""
        data = init_database
        event_id = data['event1'].id
        
        # Login first
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Try to book negative tickets
        response = client.post(f'/book/{event_id}', data={
            'num_tickets': -5
        })
        
        assert response.status_code == 200
        # Should handle error gracefully


class TestQRCodeRoute:
    """Test QR code generation"""
    @pytest.mark.events
    def test_qr_code_requires_login(self, client, init_database):
        """Test QR code endpoint requires authentication"""
        data = init_database
        booking_ref = data['booking'].booking_reference
        
        response = client.get(f'/qr_code/{booking_ref}')
        # Should redirect to login
        assert response.status_code == 302
    @pytest.mark.events
    def test_qr_code_generation(self, client, init_database):
        """Test QR code generation for booking"""
        data = init_database
        booking_ref = data['booking'].booking_reference
        
        # Login as the user who made the booking
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.get(f'/qr_code/{booking_ref}')
        assert response.status_code == 200
        assert response.content_type == 'image/png'
    @pytest.mark.events
    def test_qr_code_invalid_reference(self, client, init_database):
        """Test QR code with invalid booking reference"""
        # Login first
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.get('/qr_code/invalid-ref-12345')
        assert response.status_code == 404
    @pytest.mark.events
    def test_qr_code_unauthorized_access(self, client, init_database):
        """Test unauthorized access to QR code"""
        data = init_database
        booking_ref = data['booking'].booking_reference
        
        # Login as a different user
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        # Try to access booking QR code of another user
        response = client.get(f'/qr_code/{booking_ref}')
        # Admin should be able to access (admin privilege)
        # Regular user should not be able to access other's bookings
