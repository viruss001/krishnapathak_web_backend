from django.urls import path
from .views import (
    SignupView,
    LoginView,
    # VerifyOtpView,
    LogoutView,
    checkUser,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    # path("verify-otp/", VerifyOtpView.as_view(), name="verify-otp"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("check-user/", checkUser, name="check-user"),
]
