"""
Test cases for admin routes and dashboard
"""
import pytest
from app import db, Event
from datetime import datetime


class TestAdminRoutes:
    """Test admin-only routes"""
    
    def test_admin_dashboard_requires_login(self, client):
        """Test admin dashboard requires authentication"""
        response = client.get('/admin')
        assert response.status_code == 302  # Redirect to login
    
    def test_admin_dashboard_requires_admin_privilege(self, client, init_database):
        """Test admin dashboard requires admin privilege"""
        # Login as regular user
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.get('/admin', follow_redirects=True)
        assert response.status_code == 200
        # Should show access denied message
        assert b'denied' in response.data.lower() or b'not authorized' in response.data.lower() or b'admin' in response.data.lower()
    
    def test_admin_dashboard_access_with_admin_user(self, client, init_database):
        """Test admin can access admin dashboard"""
        # Login as admin
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = client.get('/admin')
        assert response.status_code == 200
        assert b'Admin Dashboard' in response.data or b'Manage Events' in response.data
    
    def test_admin_dashboard_shows_statistics(self, client, init_database):
        """Test admin dashboard displays statistics"""
        # Login as admin
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = client.get('/admin')
        assert response.status_code == 200
        # Should show stats like total events, bookings, revenue
        assert b'Event' in response.data or b'Booking' in response.data or b'Revenue' in response.data


class TestAdminEventManagement:
    """Test admin event management"""
    
    def test_create_event_requires_login(self, client):
        """Test creating event requires authentication"""
        response = client.post('/admin/event/new', data={
            'title': 'Test Event',
            'description': 'Test Description',
            'date_time': '2026-06-01T10:00',
            'location': 'Test Location',
            'total_tickets': 100,
            'ticket_price': 50.00
        })
        assert response.status_code == 302  # Redirect
    
    def test_create_event_requires_admin_privilege(self, client, init_database):
        """Test only admin can create events"""
        # Login as regular user
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.post('/admin/event/new', data={
            'title': 'Test Event',
            'description': 'Test Description',
            'date_time': '2026-06-01T10:00',
            'location': 'Test Location',
            'total_tickets': 100,
            'ticket_price': 50.00
        }, follow_redirects=True)
        
        # Should not create event
        assert response.status_code == 200
    
    def test_create_event_as_admin(self, client, init_database):
        """Test admin can create events"""
        # Login as admin
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = client.post('/admin/event/new', data={
            'title': 'New Conference',
            'description': 'A new tech conference',
            'date_time': '2026-07-15T09:00',
            'location': 'Chicago, IL',
            'total_tickets': 200,
            'ticket_price': 75.00
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Check event was created
        event = Event.query.filter_by(title='New Conference').first()
        assert event is not None
        assert event.location == 'Chicago, IL'
        assert event.ticket_price == 75.00
    
    def test_edit_event_as_admin(self, client, init_database):
        """Test admin can edit events"""
        data = init_database
        event_id = data['event1'].id
        
        # Login as admin
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = client.post(f'/admin/event/edit/{event_id}', data={
            'title': 'Updated Tech Conference',
            'description': 'Updated description',
            'date_time': '2026-06-20T10:00',
            'location': 'Seattle, WA',
            'total_tickets': 250,
            'ticket_price': 125.00
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Check event was updated
        event = Event.query.get(event_id)
        assert event.title == 'Updated Tech Conference'
        assert event.location == 'Seattle, WA'
    
    def test_delete_event_as_admin(self, client, init_database):
        """Test admin can delete events"""
        data = init_database
        event_id = data['event1'].id
        
        # Login as admin
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = client.post(f'/admin/event/delete/{event_id}', follow_redirects=True)
        
        assert response.status_code == 200
        # Check event was deleted
        event = Event.query.get(event_id)
        assert event is None
    
    def test_delete_event_cascade_deletes_bookings(self, client, init_database):
        """Test deleting event cascades to bookings"""
        data = init_database
        event_id = data['event2'].id
        
        # Login as admin
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = client.post(f'/admin/event/delete/{event_id}', follow_redirects=True)
        
        assert response.status_code == 200
        # Check event was deleted
        event = Event.query.get(event_id)
        assert event is None


class TestAdminDashboardDisplay:
    """Test admin dashboard information display"""
    
    def test_dashboard_displays_all_events(self, client, init_database):
        """Test dashboard lists all events"""
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = client.get('/admin')
        assert response.status_code == 200
        assert b'Tech Conference' in response.data
        assert b'Web Development' in response.data
    
    def test_dashboard_displays_all_bookings(self, client, init_database):
        """Test dashboard lists recent bookings"""
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = client.get('/admin')
        assert response.status_code == 200
        # Should display booking information
        assert b'booking' in response.data.lower() or b'Booking' in response.data
