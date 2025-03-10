from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            username = payload.get("username")
            role = payload.get("role")  # ✅ Get role from token

            if not user_id or not username or not role:
                raise AuthenticationFailed("Invalid token payload")

            User = get_user_model()
            user = User(id=user_id, username=username, is_active=True)
            user.role = role  # ✅ Dynamically add role to user

            return (user, None)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid token")