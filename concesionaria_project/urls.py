from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin de Django
    path("admin/", admin.site.urls),
    
    # Tus URLs de la app de autos
    # Asegúrate de que el archivo cars/urls.py tenga definidos los 'name'
    path("", include("cars.urls")),
]

# Servir archivos estáticos y multimedia en DESARROLLO
# Esto es CRÍTICO para que los logos y fotos de autos se vean
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)