from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, NewPasswordSerializer, EmailSerializer, PasswordResetCodeSerializer, UserUpdateSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import User

User = get_user_model()

class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            Token.objects.filter(user=user).delete()
            new_token = Token.objects.create(user=user)
            user_data = UserSerializer(user).data
            return Response({"token": new_token.key, "user":user_data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def password_reset_request(self,request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "error": "User with this email not found"
            }, status=status.HTTP_404_NOT_FOUND)

        reset_code = get_random_string(length=6, allowed_chars="0123456789")

        try:
            send_mail(
                "Your password reset code",
                f"Your password reset code is: {reset_code}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({
                "error": f"Failed to send reset code email. Error is: {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user.password_reset_code = reset_code
        user.reset_code_created_at = timezone.now()
        user.save()

        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verificate_email(self, request):
        email_serializer = EmailSerializer(data={"email": request.data.get("email")})
        email_serializer.is_valid(raise_exception=True)
        email = email_serializer.validated_data['email']

        code_serializer = PasswordResetCodeSerializer(data={"code": request.data.get("code")})
        code_serializer.is_valid(raise_exception=True)
        code = code_serializer.validated_data['code']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "error": "User does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        if not user.password_reset_code or not user.reset_code_created_at:
            return Response({
                "error": "No valid reset code found for this user."
            }, status=status.HTTP_400_BAD_REQUEST)

        if user.password_reset_code != code:
            return Response({
                "error": "Invalid reset code."
            }, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() - user.reset_code_created_at > timedelta(seconds=90):
            user.password_reset_code = None
            user.reset_code_created_at = None
            user.save()
            return Response({
                "error": "Reset code has expired"
            }, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.password_reset_code = None
        user.save()

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def password_reset_confirm(self, request):

        new_password_serializer = NewPasswordSerializer(data={"new_password": request.data.get("new_password")})
        new_password_serializer.is_valid(raise_exception=True)

        email_serializer = EmailSerializer(data={"email": request.data.get("email")})
        email_serializer.is_valid(raise_exception=True)

        new_password = new_password_serializer.validated_data['new_password']
        email = email_serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "error": "User with this email not found"
            }, status=status.HTTP_404_NOT_FOUND)

        if check_password(new_password, user.password):
            return Response({
                "error": "New password cannot be the same as the old password"
            }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({
            "message": "Your password has been successfully reset"
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def update_user(self, request):
        serializer = UserUpdateSerializer(instance=request.user, partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

