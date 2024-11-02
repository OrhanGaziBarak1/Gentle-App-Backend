from django.contrib import admin
from django.urls import path, include
from geminiApi.views import GeminiViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# router.register("", GeminiViewSet, basename='gemini')

# urlpatterns = router.urls

GeminiViewSet = GeminiViewSet.as_view({'get':'list'})

urlpatterns=[
    path('gemini/<str:chemical>/',GeminiViewSet,name='gemini')
]
