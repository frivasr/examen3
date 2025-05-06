from django.contrib.auth.models import User
from django.db import models

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    is_tecnico = models.BooleanField(default=False)
    # Puedes añadir más campos específicos del perfil aquí en el futuro

    def __str__(self):
        return f'Perfil de {self.usuario.username}'