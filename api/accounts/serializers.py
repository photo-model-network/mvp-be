from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'email', 'type', 'real_name', 'phone_number']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data.get('name', '익명의 사용자'),
            email=validated_data['email'],
            type=validated_data.get('type', None),
            real_name=validated_data.get('real_name', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = self.context.get('user')
        if user:
            return {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'avatar': user.avatar,
                'email': user.email,
                'type': user.type,
                'is_approved': user.is_approved,
                'real_name': user.real_name,
                'phone_number': user.phone_number,
                'is_identified': user.is_identified,
                'bank_account': user.bank_account,
                'bank_code': user.bank_code,
                'bank_verified': user.bank_verified,
                'business_license_number': user.business_license_number,
                'is_business': user.is_business,
                'has_studio': user.has_studio,
            }
        return None

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            self.context['user'] = user
            return data
        raise serializers.ValidationError("유효하지 않은 자격 증명입니다.")

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