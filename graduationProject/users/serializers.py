from django.core.validators import validate_email
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'full_name', 'age', 'skin_type', 'skin_problem')

    def validate_email(self, value):
        try:
            validate_email(value)
        except:
            raise serializers.ValidationError("Invalid email format.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")

        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            full_name = validated_data['full_name'],
            age=validated_data.get('age'),
            skin_type=validated_data.get('skin_type'),
            skin_problem=validated_data.get('skin_problem')
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class PasswordResetConfirmSerializer(serializers.Serializer):
    reset_code = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username", "email", 'full_name', "skin_type", "skin_problem", "age"]

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username", 'full_name', "skin_type", "skin_problem", "age"]
