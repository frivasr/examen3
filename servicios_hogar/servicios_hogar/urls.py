
from django.contrib import admin
from django.urls import path, include
# from . import views  # Comenta o elimina esta línea
from servicios import views as servicios_views # Importa las vistas de la app 'servicios'
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('servicios/', include('servicios.urls', namespace='servicios')),
    path('', servicios_views.home, name='pagina_principal'),
    path('api/token/', obtain_auth_token, name='api_token'),
]