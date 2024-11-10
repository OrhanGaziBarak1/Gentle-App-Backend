from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SkinProblemViewSet, SkinTypeViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'skin_problems', SkinProblemViewSet, basename='skin_problems')
router.register(r'skin_types', SkinTypeViewSet, basename='skin_types')

urlpatterns = [
    path('', include(router.urls)),
]
