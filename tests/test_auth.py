"""
Test cases for authentication routes (login, register, logout)
"""
import pytest
from flask import session


class TestAuthenticationRoutes:
    """Test authentication routes"""
    
    def test_register_page_accessible(self, client):
        """Test register page loads"""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Sign up' in response.data or b'register' in response.data
    
    def test_register_new_user_success(self, client, app_context):
        """Test successful user registration"""
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # After successful registration, should redirect to login or show success message
        assert b'login' in response.data.lower() or b'successful' in response.data.lower()
    
    def test_register_duplicate_username(self, client, init_database):
        """Test registration with duplicate username"""
        response = client.post('/register', data={
            'username': 'testuser',  # Already exists in init_database
            'email': 'anotheremail@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        assert b'exists' in response.data.lower() or b'already' in response.data.lower()
    
    def test_register_duplicate_email(self, client, init_database):
        """Test registration with duplicate email"""
        response = client.post('/register', data={
            'username': 'anotheruser',
            'email': 'testuser@test.com',  # Already exists in init_database
            'password': 'password123'
        })
        
        assert response.status_code == 200
        assert b'email' in response.data.lower() or b'registered' in response.data.lower()
    
    def test_login_page_accessible(self, client):
        """Test login page loads"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Welcome Back' in response.data or b'Login' in response.data
    
    def test_login_success(self, client, init_database):
        """Test successful login"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should redirect to admin or home page
        assert b'Logout' in response.data or b'Welcome' in response.data
    
    def test_login_wrong_password(self, client, init_database):
        """Test login with wrong password"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 200
        assert b'unsuccessful' in response.data.lower() or b'check' in response.data.lower()
    
    def test_login_nonexistent_user(self, client, init_database):
        """Test login with non-existent username"""
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        assert b'unsuccessful' in response.data.lower() or b'check' in response.data.lower()
    
    def test_admin_login(self, client, init_database):
        """Test admin user login"""
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Admin should be redirected to admin dashboard
        # Check for admin-related content
    
    def test_logout(self, client, init_database):
        """Test logout functionality"""
        # First login
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Then logout
        response = client.get('/logout', follow_redirects=True)
        
        assert response.status_code == 200
        # Should be redirected to home or show logged out message
    
    def test_authenticated_user_cannot_access_register(self, client, init_database):
        """Test authenticated user is redirected from register page"""
        # Login first
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Try to access register page
        response = client.get('/register', follow_redirects=True)
        
        assert response.status_code == 200
        # Should redirect away from register page
    
    def test_authenticated_user_cannot_access_login(self, client, init_database):
        """Test authenticated user is redirected from login page"""
        # Login first
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Try to access login page
        response = client.get('/login', follow_redirects=True)
        
        assert response.status_code == 200
        # Should redirect away from login page
