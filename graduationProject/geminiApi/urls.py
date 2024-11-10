from django.urls import path
from geminiApi.views import GeminiViewSet

urlpatterns=[
    path('gemini/<str:chemical>/',GeminiViewSet.as_view({'get':'list'}))
]
