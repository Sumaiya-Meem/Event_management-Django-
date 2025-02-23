from django.urls import path
from django.http import HttpResponse

from events.views import admin_dashboard,home_page,event_page

urlpatterns = [
   path('dashboard/',admin_dashboard,name='admin_dashboard'),
   path('home/',home_page,name='home_page'),
   path('event_page/',event_page,name='event_page')
]
