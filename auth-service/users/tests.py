from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import CustomUser
import json

User = get_user_model()

class UserTests(APITestCase):

    def setUp(self):
        """Setup initial test data"""
        self.admin_user = CustomUser.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="admin123",
            role="admin"
        )
        self.manager_user = CustomUser.objects.create_user(
            username="manageruser",
            email="manager@example.com",
            password="manager123",
            role="manager"
        )
        self.regular_user = CustomUser.objects.create_user(
            username="regularuser",
            email="user@example.com",
            password="user123",
            role="user"
        )
    def test_create_users(self):
        """Test if users are created successfully"""
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(self.admin_user.role, "admin")  # Change "Admin" to "admin"
        self.assertEqual(self.manager_user.role, "manager")
        self.assertEqual(self.regular_user.role, "user")


    def test_user_login(self):
        """Test login functionality"""
        url = reverse("token_obtain_pair")  # ✅ Ensure correct JWT login URL
        data = {"username": "adminuser", "password": "admin123"}
        
        response = self.client.post(
            url,
            data=json.dumps(data),  # ✅ Convert dictionary to JSON string
            content_type="application/json"  # ✅ Ensure JSON format
        )

        print("Response Status Code:", response.status_code)
        print("Response Data:", response.content)  # ✅ Debugging response

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # ✅ Ensure JWT token is returned