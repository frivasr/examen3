# usuarios/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import PerfilUsuario

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)
        Token.objects.create(user=instance)  # Crea un token al crear el usuario

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    try:
        instance.perfil.save()
    except PerfilUsuario.DoesNotExist:
        PerfilUsuario.objects.create(usuario=instance)
        Token.objects.create(user=instance) # Asegura que si no existe perfil, también se crea token