from rest_framework import serializers
from django.core.validators import RegexValidator

class GoogleSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class KakaoSerializer(serializers.Serializer):
    pass


class NaverSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    state = serializers.CharField(required=True)


class BusinessVerificationSerializer(serializers.Serializer):
    businessNum = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='사업자 번호는 반드시 10자리 숫자여야 합니다.',
                code='invalid_businessNum'
            )
        ]
    )