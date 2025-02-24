from django.urls import path
from .views import admin_dashboard, home_page, event_page, create_event, create_category,create_participant,admin_home

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('home/', home_page, name='home_page'),
    path('event_page/', event_page, name='event_page'),
    path('dashboard/create-event/', create_event, name='create-event'),
    path('dashboard/create-category/', create_category, name='create-category'),
    path('dashboard/create-participant/', create_participant, name='create-participant'),
    path('dashboard/admin-home',admin_home , name='admin-home'),
]