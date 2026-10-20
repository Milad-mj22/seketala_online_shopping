from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('api/voice-assistant/', views.voice_assistant, name='voice_assistant'),
    path('verify/', views.verify, name='verify'),
    path('callback/', views.top_callback, name='verify'),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]