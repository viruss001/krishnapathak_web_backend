from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.decorators import api_view, permission_classes, authentication_classes
import jwt

from .models import UserToken
from .utils import generate_jwt_for_superuser


# -------------------- SIGNUP --------------------

class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("name")
        # last_name = request.data.get("last_name")

        if not all([email, password, first_name]):
            return Response({"error": "Email, password, first name, and last name are required."}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered."}, status=400)

        username = email.split("@")[0]

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            # last_name=last_name
        )

        return Response({"message": "User created successfully"}, status=201)


# -------------------- LOGIN --------------------

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not all([email, password]):
            return Response({"error": "Email and password are required"}, status=400)

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=401)

        user = authenticate(request, username=user_obj.username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        login(request, user)

        # ✅ Generate JWT only if superuser
        token = None
        if user.is_superuser:
            token = generate_jwt_for_superuser(user)

        return Response({
            "message": "Login successful",
            "is_superuser": user.is_superuser,
            "token": token
        }, status=200)


# -------------------- LOGOUT --------------------

class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        token = request.data.get("jwt")
        if not token:
            return Response({"error": "Token missing"}, status=400)

        UserToken.objects.filter(token=token).delete()
        logout(request)

        return Response({"message": "Logged out successfully"}, status=200)


# -------------------- CHECK USER (JWT VALIDATION) --------------------

@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def checkUser(request):
    token = request.data.get("jwt")

    if not token:
        return Response({"error": "Token missing"}, status=400)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        exists = UserToken.objects.filter(user_id=payload["user_id"], token=token).exists()
        if not exists:
            return Response({"error": "Token not recognized"}, status=401)

        return Response({
            "user_id": payload["user_id"],
            "username": payload["username"],
            "is_superuser": payload["is_superuser"],
            "valid": True
        }, status=200)

    except ExpiredSignatureError:
        return Response({"error": "Token expired"}, status=401)
    except InvalidTokenError:
        return Response({"error": "Invalid token"}, status=401)
