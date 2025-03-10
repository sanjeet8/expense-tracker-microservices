from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class RoleBasedAccessTest(APITestCase):
    def setUp(self):
        # Create Admin User
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpassword"
        )
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)

        # Create Regular User
        self.regular_user = User.objects.create_user(
            username="user", email="user@example.com", password="userpassword"
        )
        self.regular_token = str(RefreshToken.for_user(self.regular_user).access_token)

    def test_admin_can_view_all_expenses(self):
        print(f"DEBUG: Admin token -> {self.admin_token}")  # Add this line
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get("/api/expenses/")
        print(f"DEBUG: Response status -> {response.status_code}, Response data -> {response.data}")  # Debugging
        self.assertEqual(response.status_code, 200)


    def test_regular_user_can_only_view_own_expenses(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_token}")
        response = self.client.get("/api/expenses/")
        self.assertEqual(response.status_code, 200)  # Expect success
