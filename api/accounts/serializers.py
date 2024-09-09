from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[
        RegexValidator(
            regex='^(?=.*[A-Z])(?=.*\d).{8,}$',
            message='비밀번호는 최소 8자 이상이어야 하며, 하나 이상의 대문자와 숫자를 포함해야 합니다.'
        )
    ])

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'email', 'real_name', 'phone_number']
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 존재하는 사용자 이름입니다.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data.get('name', '익명의 사용자'),
            email=validated_data['email'],
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


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[
        RegexValidator(
            regex='^(?=.*[A-Z])(?=.*\d).{8,}$',
            message='비밀번호는 최소 8자 이상이어야 하며, 하나 이상의 대문자와 숫자를 포함해야 합니다.'
        )
    ])

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 올바르지 않습니다.")
        return value

    def validate(self, data):
        if data['current_password'] == data['new_password']:
            raise serializers.ValidationError("새 비밀번호는 현재 비밀번호와 달라야 합니다.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


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