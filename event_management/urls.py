
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from debug_toolbar.toolbar import debug_toolbar_urls
# from tasks.views import

def home_view(request):
    return HttpResponse("Welcome to Event Management!")

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', home_view, name='home'),
     path('events/', include("events.urls")),
]+ debug_toolbar_urls()
