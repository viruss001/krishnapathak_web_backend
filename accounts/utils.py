# utils.py
import datetime
import jwt

from django.conf import settings
from .models import UserToken
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError



def generate_jwt_for_superuser(user, response=None):
    """
    Generate JWT for superuser and store it in DB.
    (Doesn't use cookies or headers.)
    """
    if not user.is_superuser:
        return None

    payload = {
        "user_id": user.id,
        "username": user.username,
        "is_superuser": user.is_superuser,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    # Remove old tokens and save new one
    UserToken.objects.filter(user=user).delete()
    UserToken.objects.create(user=user, token=token)

    return token


def checkUserIsAuthenticated(request):
    token = request.COOKIES.get("jwt")
    if not token:
        return False

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return UserToken.objects.filter(user_id=payload["user_id"], token=token).exists()
    except (ExpiredSignatureError, InvalidTokenError):
        return False
