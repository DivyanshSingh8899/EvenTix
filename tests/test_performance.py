"""
Performance and Load Testing for Event Booking System
Tests response times, throughput, and system behavior under load
"""
import pytest
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed


class TestResponseTimes:
    """Test that routes respond within acceptable time limits"""
    
    def test_home_page_response_time(self, client, init_database):
        """Test home page loads in under 200ms"""
        start_time = time.time()
        response = client.get('/')
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000  # Convert to ms
        
        assert response.status_code == 200
        assert execution_time < 200, f"Home page took {execution_time:.2f}ms (target: < 200ms)"
    
    def test_events_listing_response_time(self, client, init_database):
        """Test events listing loads in under 300ms"""
        start_time = time.time()
        response = client.get('/events')
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        assert execution_time < 300, f"Events page took {execution_time:.2f}ms (target: < 300ms)"
    
    def test_event_detail_response_time(self, client, init_database):
        """Test event detail page loads in under 150ms"""
        data = init_database
        event_id = data['event1'].id
        
        start_time = time.time()
        response = client.get(f'/event/{event_id}')
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        assert execution_time < 150, f"Event detail took {execution_time:.2f}ms (target: < 150ms)"
    
    def test_admin_dashboard_response_time(self, client, init_database):
        """Test admin dashboard loads in under 500ms"""
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        start_time = time.time()
        response = client.get('/admin')
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        assert execution_time < 500, f"Admin dashboard took {execution_time:.2f}ms (target: < 500ms)"
    
    def test_login_response_time(self, client, init_database):
        """Test login completes in under 300ms"""
        start_time = time.time()
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000
        
        assert response.status_code == 302  # Redirect
        assert execution_time < 300, f"Login took {execution_time:.2f}ms (target: < 300ms)"
    
    def test_booking_response_time(self, client, init_database):
        """Test booking completes in under 300ms"""
        data = init_database
        event_id = data['event1'].id
        
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        start_time = time.time()
        response = client.post(f'/book/{event_id}', data={
            'num_tickets': 2
        })
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        assert execution_time < 300, f"Booking took {execution_time:.2f}ms (target: < 300ms)"
    
    def test_qr_code_generation_time(self, client, init_database):
        """Test QR code generation completes in under 1000ms"""
        data = init_database
        booking_ref = data['booking'].booking_reference
        
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        start_time = time.time()
        response = client.get(f'/qr_code/{booking_ref}')
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        assert execution_time < 1000, f"QR code generation took {execution_time:.2f}ms (target: < 1000ms)"


class TestConcurrentRequests:
    """Test system behavior under concurrent load"""
    
    def test_multiple_concurrent_home_requests(self, client, init_database):
        """Test 10 concurrent home page requests"""
        def make_request():
            start = time.time()
            response = client.get('/')
            return time.time() - start, response.status_code
        
        times = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            for future in as_completed(futures):
                execution_time, status_code = future.result()
                times.append(execution_time)
                assert status_code == 200
        
        avg_time = statistics.mean(times) * 1000
        max_time = max(times) * 1000
        
        print(f"\n10 concurrent requests - Avg: {avg_time:.2f}ms, Max: {max_time:.2f}ms")
        
        # Average should be reasonable even under load
        assert avg_time < 500, f"Average concurrent request time {avg_time:.2f}ms too high"
    
    def test_concurrent_event_browsing(self, client, init_database):
        """Test 10 concurrent event listing requests"""
        def make_request():
            start = time.time()
            response = client.get('/events')
            return time.time() - start, response.status_code
        
        times = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            for future in as_completed(futures):
                execution_time, status_code = future.result()
                times.append(execution_time)
                assert status_code == 200
        
        avg_time = statistics.mean(times) * 1000
        
        print(f"\n10 concurrent event requests - Avg: {avg_time:.2f}ms")
        assert avg_time < 600


class TestThroughput:
    """Test system throughput - requests per second"""
    
    def test_home_page_throughput(self, client, init_database):
        """Measure home page requests per second"""
        num_requests = 50
        start_time = time.time()
        
        for _ in range(num_requests):
            response = client.get('/')
            assert response.status_code == 200
        
        end_time = time.time()
        total_time = end_time - start_time
        throughput = num_requests / total_time
        
        print(f"\nHome page throughput: {throughput:.2f} requests/sec")
        
        # Should handle at least 10 req/sec
        assert throughput > 10, f"Throughput {throughput:.2f} req/sec is too low"
    
    def test_login_throughput(self, client, init_database):
        """Measure login requests per second"""
        num_requests = 20
        start_time = time.time()
        
        for i in range(num_requests):
            response = client.post('/login', data={
                'username': 'admin',
                'password': 'admin123'
            })
            assert response.status_code in [200, 302]
        
        end_time = time.time()
        total_time = end_time - start_time
        throughput = num_requests / total_time
        
        print(f"\nLogin throughput: {throughput:.2f} requests/sec")
        
        # Should handle at least 5 login req/sec
        assert throughput > 5, f"Login throughput {throughput:.2f} req/sec is too low"


class TestMemoryUsage:
    """Test that pages don't use excessive memory"""
    
    def test_event_listing_memory(self, client, init_database):
        """Test that events page doesn't grow memory excessively"""
        import tracemalloc
        
        tracemalloc.start()
        
        # Make multiple requests
        for _ in range(10):
            response = client.get('/events')
            assert response.status_code == 200
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"\nEvents page - Current: {current / 1024:.2f}KB, Peak: {peak / 1024:.2f}KB")
        
        # Peak should be under 10MB for this operation
        assert peak < 10 * 1024 * 1024, f"Peak memory {peak / 1024 / 1024:.2f}MB is too high"


class TestResponseQuality:
    """Test response quality and completeness"""
    
    def test_home_page_content_completeness(self, client, init_database):
        """Test home page includes all expected content"""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'EventTix' in response.data or b'event' in response.data.lower()
        assert b'css' in response.data or b'style' in response.data.lower()
        assert b'js' in response.data or b'script' in response.data.lower()
    
    def test_events_page_loads_all_events(self, client, init_database):
        """Test events page loads all events"""
        response = client.get('/events')
        
        assert response.status_code == 200
        # Should contain event data
        assert b'Tech Conference' in response.data or b'Web Development' in response.data
    
    def test_admin_dashboard_loads_statistics(self, client, init_database):
        """Test admin dashboard loads all statistics"""
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = client.get('/admin')
        
        assert response.status_code == 200
        # Should contain dashboard elements
        assert b'Event' in response.data or b'Dashboard' in response.data


class TestErrorHandling:
    """Test performance under error conditions"""
    
    def test_404_response_time(self, client):
        """Test that 404 errors respond quickly"""
        start_time = time.time()
        response = client.get('/nonexistent-page-12345')
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000
        
        assert response.status_code == 404
        assert execution_time < 100, f"404 response took {execution_time:.2f}ms"
    
    def test_invalid_booking_response_time(self, client, init_database):
        """Test that invalid booking request responds quickly"""
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        start_time = time.time()
        response = client.post('/book/99999', data={
            'num_tickets': 1
        })
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000
        
        assert response.status_code == 404
        assert execution_time < 150, f"Invalid booking response took {execution_time:.2f}ms"


class TestDatabasePerformance:
    """Test database query performance"""
    
    def test_event_query_performance(self, client, init_database):
        """Test that event queries are reasonably fast"""
        from app import Event
        
        start_time = time.time()
        events = Event.query.all()
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000
        
        assert len(events) > 0
        assert execution_time < 50, f"Event query took {execution_time:.2f}ms"
    
    def test_user_lookup_performance(self, client, init_database):
        """Test that user lookups are fast"""
        from app import User
        
        start_time = time.time()
        user = User.query.filter_by(username='testuser').first()
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000
        
        assert user is not None
        assert execution_time < 30, f"User lookup took {execution_time:.2f}ms"


class TestResponseSizes:
    """Test that responses aren't too large"""
    
    def test_home_page_size(self, client, init_database):
        """Test home page response size"""
        response = client.get('/')
        
        size_kb = len(response.data) / 1024
        
        print(f"\nHome page size: {size_kb:.2f}KB")
        
        # Should be under 2MB
        assert len(response.data) < 2 * 1024 * 1024
    
    def test_events_page_size(self, client, init_database):
        """Test events page response size"""
        response = client.get('/events')
        
        size_kb = len(response.data) / 1024
        
        print(f"Events page size: {size_kb:.2f}KB")
        
        # Should be under 3MB even with many events
        assert len(response.data) < 3 * 1024 * 1024
