from django.urls import path
from django.http import HttpResponse

from events.views import admin_dashboard,home_page

urlpatterns = [
   path('dashboard/',admin_dashboard),
   path('home/',home_page)
]
