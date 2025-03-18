from django.urls import path
from geminiApi.views import GeminiViewSet

urlpatterns=[
    path('gemini/',GeminiViewSet.as_view({'post':'list'}))
]
