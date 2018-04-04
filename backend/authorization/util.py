from datetime import timedelta

from django.utils import timezone
from django_gravatar.helpers import get_gravatar_url
from refreshtoken.models import RefreshToken
from rest_framework.authtoken.models import Token

from swipe import settings


def get_auth_token(header: str):
    if header.lower().startswith("token "):
        tokens = Token.objects.filter(key=header[6:])
        if tokens.count() == 1:
            return tokens.first()
    return None


def get_token_expiry(token: Token):
    return (timezone.now() if token.created is None else token.created) + timedelta(
        hours=settings.AUTH_TOKEN_VALID_TIME_HOURS)


def is_token_expired(token: Token) -> bool:
    return get_token_expiry(token) < timezone.now()


def jwt_response_payload_handler(token, user=None, request=None):
    if user is None:
        return {
            'token': token
        }

    try:
        refresh_token = user.refresh_tokens.get(app='swipe').key
    except RefreshToken.DoesNotExist:
        refresh_token = None

    return {
        'token': token,
        'refresh_token': refresh_token,
        'valid': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'permissions': user.get_all_permissions(),
            'gravatarUrl': get_gravatar_url(user.email),
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
        }
    }
