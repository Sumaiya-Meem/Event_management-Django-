
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from debug_toolbar.toolbar import debug_toolbar_urls
from events.views import home_page
# from tasks.views import


urlpatterns = [
    path('admin/', admin.site.urls),
     path('', home_page, name='home'),
     path('events/', include("events.urls")),
     path("users/", include("users.urls")),
]+ debug_toolbar_urls()
