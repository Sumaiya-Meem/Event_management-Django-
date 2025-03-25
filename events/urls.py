from django.urls import path
from .views import  home_page, event_page, create_event, create_category,admin_home,event_detail,update_event,update_category,delete_event,delete_category,user_list,assign_role,create_group,group_list,delete_group,rsvp_event,participant_dashboard,organizer_dashboard,user_dashboard,dashboard,delete_user

urlpatterns = [
    # path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('home/', home_page, name='home_page'),
    path('event_page/', event_page, name='event_page'),
     path('event/<int:id>/',event_detail, name='event-detail'),
    path('create-event/', create_event, name='create-event'),
    path('create-category/', create_category, name='create-category'),
    # path('create-participant/', create_participant, name='create-participant'),
    path('admin-home',admin_home , name='admin-home'),
     path("organizer-dashboard/",organizer_dashboard,name="organizer-dashboard"),
     path("user-dashboard/",user_dashboard,name="user-dashboard"),
    path("update-event/<int:id>/",update_event,name="update-event"),
    path("update-category/<int:id>/",update_category,name="update-category"),
    path("delete_event/<int:id>/",delete_event,name="delete-event"),
    path("delete_category/<int:id>/",delete_category,name="delete-category"),
    # path("delete_participant/<int:id>/",delete_participant,name="delete-participant"),
    # path("update_participant/<int:id>/",update_participant,name="update-participant"),
    path("user_list/",user_list,name="user-list"),
    path('delete-user/<int:user_id>/', delete_user, name='delete-user'),
    path('admin/<int:user_id>/assign-role', assign_role, name='assign-role'),
    path('admin/create-group', create_group, name='create-group'),
    path('admin/group-list', group_list, name='group-list'),
    path('admin/<int:group_id>/delete-group',delete_group, name='delete-group'),
    path('admin/rsvp/<int:event_id>/', rsvp_event, name='rsvp-event'),
    path('admin/participant-dashboard/', participant_dashboard, name='participant-dashboard'),
    path('dashboard/', dashboard, name='dashboard'),
    
]