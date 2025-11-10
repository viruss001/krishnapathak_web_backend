from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.decorators import api_view, permission_classes, authentication_classes

import jwt

from .models import UserToken, Otp
from .utils import generate_jwt_for_superuser
from utils import otp, sendmail
from .serializers import VerifyOtpSerializer


# -------------------- SIGNUP --------------------


class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not all([email, password]):
            return Response({"error": "Email and password are required"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered"}, status=400)

        username = email.split("@")[0]
        User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "User created successfully"}, status=201)


# -------------------- LOGIN (Step 1: Send OTP) --------------------

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

        otp_code = otp.generate_otp()
        Otp.objects.update_or_create(
            email=email,
            defaults={"otp": otp_code, "exp": timezone.now() + timedelta(minutes=20)}
        )

        sendmail.send_otp_email_task(email, otp_code)

        return Response({"message": "OTP sent to email"}, status=200)


# -------------------- VERIFY OTP (Step 2: Issue JWT) --------------------

class VerifyOtpView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp_code = serializer.validated_data["otp"]

            try:
                otp_entry = Otp.objects.get(email=email)
            except Otp.DoesNotExist:
                return Response({"error": "OTP not found"}, status=404)

            if otp_entry.is_expired():
                return Response({"error": "OTP expired"}, status=400)

            if otp_entry.otp != otp_code:
                return Response({"error": "Invalid OTP"}, status=400)

            otp_entry.delete()

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

            login(request, user)

            # ✅ generate token for superuser
            token = None
            if user.is_superuser:
                token = generate_jwt_for_superuser(user)

            return Response({
                "message": "Login successful",
                "token": token,  # returned to frontend
                "is_superuser": user.is_superuser
            }, status=200)

        print(serializer.errors)
        return Response(serializer.errors, status=400)


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