from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import SkinProblem, SkinType
from .serializers import UserRegistrationSerializer, UserLoginSerializer, SkinProblemSerializer, SkinTypeSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response({"token": token.key, "user_id": user.id}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user:
            Token.objects.filter(user=user).delete()
            new_token = Token.objects.create(user=user)
            return Response({"token": new_token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class SkinProblemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SkinProblemSerializer
    queryset = SkinProblem.objects.all()

class SkinTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SkinTypeSerializer
    queryset = SkinType.objects.all()

