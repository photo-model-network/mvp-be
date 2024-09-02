from rest_framework import serializers


class GoogleSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class KakaoSerializer(serializers.Serializer):
    pass


class NaverSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
