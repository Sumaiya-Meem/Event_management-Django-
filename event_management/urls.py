
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from debug_toolbar.toolbar import debug_toolbar_urls
from events.views import home_page
# from tasks.views import
from django.conf.urls.static import static
from django.conf import settings
from core.views import no_permission

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', home_page, name='home'),
     path('events/', include("events.urls")),
     path("users/", include("users.urls")),
     path('no_permission/', no_permission, name='no-permission'),
]+ debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)