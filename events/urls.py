from django.urls import path
from .views import admin_dashboard, home_page, event_page, create_event, create_category,create_participant,admin_home,event_detail,update_event,update_category,delete_event,delete_category,delete_participant,update_participant

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('home/', home_page, name='home_page'),
    path('event_page/', event_page, name='event_page'),
     path('event/<int:id>/',event_detail, name='event-detail'),
    path('dashboard/create-event/', create_event, name='create-event'),
    path('dashboard/create-category/', create_category, name='create-category'),
    path('dashboard/create-participant/', create_participant, name='create-participant'),
    path('dashboard/admin-home',admin_home , name='admin-home'),
    path("update-event/<int:id>/",update_event,name="update-event"),
    path("update-category/<int:id>/",update_category,name="update-category"),
    path("delete_event/<int:id>/",delete_event,name="delete-event"),
    path("delete_category/<int:id>/",delete_category,name="delete-category"),
    path("delete_participant/<int:id>/",delete_participant,name="delete-participant"),
    path("update_participant/<int:id>/",update_participant,name="update-participant"),
]