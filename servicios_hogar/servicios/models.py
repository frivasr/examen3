from django.db import models
from django.contrib.auth.models import User





class TipoServicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class SolicitudServicio(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes')
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=255)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_preferida = models.DateField()
    estado = models.CharField(max_length=20, default='pendiente')  # Opciones: pendiente, en_proceso, completado, cancelado
    tecnico_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='asignaciones')

    def __str__(self):
        return f'Solicitud de {self.tipo_servicio} para {self.direccion} ({self.fecha_solicitud})'
    
class CalificacionServicio(models.Model):
    solicitud = models.OneToOneField(SolicitudServicio, on_delete=models.CASCADE, related_name='calificacion')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(choices=[(1, '1 estrella'), (2, '2 estrellas'), (3, '3 estrellas'), (4, '4 estrellas'), (5, '5 estrellas')])
    comentario = models.TextField(blank=True)
    fecha_calificacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('solicitud', 'cliente') # Un cliente solo puede calificar una solicitud una vez

    def __str__(self):
        return f'Calificación de {self.solicitud} por {self.cliente}'
    
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    tipo = models.CharField(max_length=50, blank=True, null=True) # Opcional: para categorizar notificaciones
    objeto_id = models.PositiveIntegerField(null=True, blank=True) # Opcional: ID del objeto relacionado

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'Notificación para {self.usuario.username} ({self.fecha_creacion})'
    
class PerfilTecnico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='perfil_tecnico')
    especialidades = models.CharField(max_length=255, blank=True)
    experiencia = models.TextField(blank=True)
    descripcion = models.TextField(blank=True)
    

    def __str__(self):
        return f'Perfil de {self.usuario.username}'
    

