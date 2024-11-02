from django.urls import path
from geminiApi.views import GeminiViewSet

GeminiViewSet = GeminiViewSet.as_view({'get':'list'})

urlpatterns=[
    path('gemini/<str:chemical>/',GeminiViewSet)
]
