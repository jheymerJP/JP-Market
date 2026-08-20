from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from cuentas import views as cuentas_views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('tienda.urls')),
    path('carrito/', include('carrito.urls')),
    path('cuentas/', include('cuentas.urls')),
    path('panel-admin/', include('panel_admin.urls', namespace='panel_admin')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
