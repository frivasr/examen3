from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # ¡Esta línea es importante!

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('registro/', views.registro_usuario, name='registro'),
    path('registro/exitoso/', views.registro_exitoso, name='registro_exitoso'),
    path('recuperar-password/', views.password_reset_request, name='password_reset_request'),
    path('password_reset/confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('perfil/', views.modificar_perfil, name='perfil'),
    path('logout/', auth_views.LogoutView.as_view(next_page='pagina_principal'), name='logout'),
   # path('servicios/', views.lista_servicios, name='lista_servicios'),
]