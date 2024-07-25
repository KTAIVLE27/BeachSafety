from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('main.urls')),
    path("control/", include('control.urls')),
    path('adminpanel/', include('adminpanel.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)