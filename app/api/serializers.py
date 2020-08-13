from rest_auth.serializers import LoginSerializer


class CustomUserLoginSerializer(LoginSerializer):
    email = None
