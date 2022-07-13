from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=32)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=32)
    first_name = serializers.CharField(min_length=2, max_length=128)
    last_name = serializers.CharField(min_length=2, max_length=128)




class RefreshResponseSwaggerSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    refresh_exp = serializers.IntegerField()
    access = serializers.CharField()
    access_exp = serializers.IntegerField()


class SendTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    refresh_exp = serializers.IntegerField()
    access = serializers.CharField()
    access_exp = serializers.IntegerField()



class TokenRefreshCustomSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        access_token = refresh.access_token
        data = {
            'access': str(access_token),
            'access_exp': access_token.get('exp')
        }

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)
            data['refresh_exp'] = refresh.get('exp')

        return data