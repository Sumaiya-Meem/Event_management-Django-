from django.urls import path
from django.http import HttpResponse

from events.views import admin_dashboard

urlpatterns = [
   path('dashboard/',admin_dashboard)
]
