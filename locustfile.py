"""
Locust Load Testing File - Simulate real user load on your website
Deploy with: locust -f locustfile.py
"""

from locust import HttpUser, task, between
import random


class WebsiteUser(HttpUser):
    """Simulates a typical website user behavior"""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Called when a user starts - like user login"""
        self.event_ids = [1, 2]  # Available event IDs
        self.logged_in = False
    
    @task(3)
    def view_home(self):
        """View home page (higher weight = more frequent)"""
        self.client.get("/")
    
    @task(5)
    def view_events(self):
        """Browse events (most users browse)"""
        self.client.get("/events")
    
    @task(3)
    def view_event_detail(self):
        """View event details"""
        event_id = random.choice(self.event_ids)
        self.client.get(f"/event/{event_id}")
    
    @task(2)
    def login(self):
        """Attempt login"""
        self.client.post("/login", {
            "username": "testuser",
            "password": "password123",
        })
        self.logged_in = True
    
    @task(1)
    def book_ticket(self):
        """Book tickets (if logged in)"""
        if self.logged_in:
            event_id = random.choice(self.event_ids)
            self.client.post(f"/book/{event_id}", {
                "num_tickets": random.randint(1, 3)
            })
    
    @task(1)
    def logout(self):
        """Logout"""
        if self.logged_in:
            self.client.get("/logout")
            self.logged_in = False


class AdminUser(HttpUser):
    """Simulates admin user behavior"""
    
    wait_time = between(2, 5)
    
    def on_start(self):
        """Admin login on start"""
        self.client.post("/login", {
            "username": "admin",
            "password": "admin123",
        })
    
    @task(10)
    def view_admin_dashboard(self):
        """Frequently check admin dashboard"""
        self.client.get("/admin")
    
    @task(3)
    def view_events(self):
        """Occasionally browse events"""
        self.client.get("/events")
    
    @task(2)
    def create_event(self):
        """Create new event"""
        self.client.post("/admin/event/new", {
            "title": f"Event {random.randint(100, 999)}",
            "description": "Test event",
            "date_time": "2026-06-01T10:00",
            "location": "Test Location",
            "total_tickets": 100,
            "ticket_price": 50.00,
        })


class MobileUser(HttpUser):
    """Simulates mobile user with slower network"""
    
    wait_time = between(2, 4)  # Mobile users take longer
    
    @task(5)
    def view_home(self):
        """Mobile users focus on home page"""
        self.client.get("/")
    
    @task(3)
    def view_events(self):
        """Browse events on mobile"""
        self.client.get("/events")
    
    @task(2)
    def view_event_detail(self):
        """View event on mobile"""
        self.client.get("/event/1")
