

from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('api/', views.submit_complaint, name='submit'),
    # مسیر نهایی: /complaints/api/
]