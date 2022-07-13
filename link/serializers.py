from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from link.models import Link


class LinkSerializer(serializers.Serializer):
    link = serializers.CharField()




class LinkResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link

class GetLink(serializers.Serializer):
    id = serializers.IntegerField()