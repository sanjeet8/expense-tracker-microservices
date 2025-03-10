from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from .permissions import IsAdmin, IsManager

User = get_user_model()

# ✅ Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# ✅ Custom JWT Token Serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        #token["password"]
        token["role"] = user.role  # ✅ Add role to token
        return token

# ✅ Custom JWT Token View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ✅ User Details API
User = get_user_model()  # ✅ Explicitly get User model from DB

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # ✅ Extract user from token instead of Django's default user model
        token_user = request.user  # Comes from JWT token
        if not token_user or not token_user.id:
            raise AuthenticationFailed("User not found")

        # ✅ If admin, return all users
        if token_user.role == "admin":
            users = User.objects.all().values("id", "username", "email", "role")
            return Response({"users": list(users)})

        # ✅ If not admin, return only the authenticated user's details
        return Response({
            "id": token_user.id,
            "username": token_user.username,
            "email": token_user.email,
            "role": token_user.role
        })

# ✅ Verify Token API
class VerifyTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"detail": "Token is required"}, status=400)

        try:
            payload = AccessToken(token)
            user = User.objects.filter(id=payload["user_id"]).first()
            if not user:
                return Response({"detail": "User not found"}, status=401)

            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            })
        except Exception:
            return Response({"detail": "Invalid token"}, status=401)

# ✅ Admin-Only View Example
class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"message": "Hello Admin!"})

# ✅ Manager & Admin View Example
class ManagerView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        return Response({"message": "Hello Manager or Admin!"})
