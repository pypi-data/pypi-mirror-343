from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from dashboard.models import UserProfile


class AuthenticationTests(TestCase):
    """
    Tests for authentication functionality
    """
    def setUp(self):
        """
        Set up test data
        """
        self.client = Client()
        self.register_url = reverse('dashboard:register')
        self.login_url = reverse('dashboard:login')
        self.logout_url = reverse('dashboard:logout')
        self.profile_url = reverse('dashboard:profile')
        self.password_change_url = reverse('dashboard:password_change')
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
    
    def test_register_view_get(self):
        """
        Test that the register view returns a 200 response for a GET request
        """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/auth/register.html')
    
    def test_register_view_post(self):
        """
        Test that a user can register
        """
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        
        # Check that the user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Check that a profile was created for the user
        user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(user, 'profile'))
        
        # Check that the user is logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_view_get(self):
        """
        Test that the login view returns a 200 response for a GET request
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/auth/login.html')
    
    def test_login_view_post_success(self):
        """
        Test that a user can log in with correct credentials
        """
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_view_post_failure(self):
        """
        Test that a user cannot log in with incorrect credentials
        """
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_logout_view(self):
        """
        Test that a user can log out
        """
        # Log in first
        self.client.login(username='testuser', password='testpassword123')
        
        # Then log out
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_profile_view_authenticated(self):
        """
        Test that an authenticated user can access the profile page
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/auth/profile.html')
    
    def test_profile_view_unauthenticated(self):
        """
        Test that an unauthenticated user is redirected to the login page
        """
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn(self.login_url, response.url)
    
    def test_password_change_authenticated(self):
        """
        Test that an authenticated user can access the password change page
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.password_change_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/auth/password_change.html')
    
    def test_password_change_unauthenticated(self):
        """
        Test that an unauthenticated user is redirected to the login page
        """
        response = self.client.get(self.password_change_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn(self.login_url, response.url)
    
    def test_password_change_success(self):
        """
        Test that a user can change their password
        """
        self.client.login(username='testuser', password='testpassword123')
        data = {
            'old_password': 'testpassword123',
            'new_password1': 'newtestpassword123',
            'new_password2': 'newtestpassword123'
        }
        response = self.client.post(self.password_change_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful password change
        
        # Check that the password was changed
        self.client.logout()
        login_success = self.client.login(username='testuser', password='newtestpassword123')
        self.assertTrue(login_success)


class UserProfileTests(TestCase):
    """
    Tests for user profile functionality
    """
    def setUp(self):
        """
        Set up test data
        """
        self.client = Client()
        self.profile_url = reverse('dashboard:profile')
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
    
    def test_profile_update(self):
        """
        Test that a user can update their profile
        """
        self.client.login(username='testuser', password='testpassword123')
        
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'bio': 'This is my updated bio',
            'position': 'Developer',
            'phone_number': '123-456-7890',
            'address': '123 Main St'
        }
        
        response = self.client.post(self.profile_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Refresh user from database
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        
        # Check that the user and profile were updated
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.profile.bio, 'This is my updated bio')
        self.assertEqual(self.user.profile.position, 'Developer')
        self.assertEqual(self.user.profile.phone_number, '123-456-7890')
        self.assertEqual(self.user.profile.address, '123 Main St')
