from abc import ABC

from rest_auth.serializers import LoginSerializer


class CustomUserLoginSerializer(LoginSerializer, ABC):
    email = None
