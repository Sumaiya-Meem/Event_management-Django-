
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
# from tasks.views import

def home_view(request):
    return HttpResponse("Welcome to Event Management!")

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', home_view, name='home'),
     path('events/', include("events.urls")),
]
