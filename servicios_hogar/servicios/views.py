from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .forms import SolicitarServicioForm, AsignarTecnicoForm, TipoServicioForm, EditarTipoServicioForm, CalificarServicioForm, PerfilTecnicoForm, GroupForm
from .forms import SolicitarServicioForm,SolicitudServicioForm
from .models import SolicitudServicio, TipoServicio, CalificacionServicio, Notificacion, PerfilTecnico
Servicio = TipoServicio
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ServicioSerializer, SolicitudServicioSerializer




class ServicioList(generics.ListAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class SolicitudServicioCreate(generics.CreateAPIView):
    queryset = SolicitudServicio.objects.all()
    serializer_class = SolicitudServicioSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class SolicitudServicioDetail(generics.RetrieveAPIView):  # Nueva vista para obtener detalles
    queryset = SolicitudServicio.objects.all()
    serializer_class = SolicitudServicioSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
@login_required
def solicitar_servicio(request):
    if request.method == 'POST':
        form = SolicitarServicioForm(request.POST)
        if form.is_valid():
            tipo_servicio = form.cleaned_data['tipo_servicio']
            descripcion = form.cleaned_data['descripcion']
            direccion = form.cleaned_data['direccion']
            fecha_preferida = form.cleaned_data['fecha_preferida']

            solicitud = SolicitudServicio(
                cliente=request.user,
                tipo_servicio=tipo_servicio,  
                descripcion=descripcion,
                direccion=direccion,
                fecha_preferida=fecha_preferida
            )
            solicitud.save()
            messages.success(request, 'Tu solicitud de servicio ha sido enviada correctamente.')
            return redirect('servicios:lista_solicitudes')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = SolicitarServicioForm()
    return render(request, 'cliente/solicitar_servicio.html', {'form': form})

@login_required
def lista_solicitudes(request):
    solicitudes = SolicitudServicio.objects.filter(cliente=request.user).order_by('-fecha_solicitud')
    return render(request, 'cliente/lista_solicitudes.html', {'solicitudes': solicitudes})

@login_required
def detalle_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudServicio, id=solicitud_id, cliente=request.user)
    return render(request, 'cliente/detalle_solicitud.html', {'solicitud': solicitud})

def listar_servicios(request):
   
    return render(request, 'servicios/listar_servicios.html')

def home(request):
    return render(request, 'home.html')

@login_required
def lista_asignaciones(request):
    asignaciones = SolicitudServicio.objects.filter(tecnico_asignado=request.user).order_by('-fecha_solicitud')
    return render(request, 'tecnico/lista_asignaciones.html', {'asignaciones': asignaciones})

@login_required
def detalle_asignacion(request, asignacion_id):
    asignacion = get_object_or_404(SolicitudServicio, id=asignacion_id, tecnico_asignado=request.user)
    return render(request, 'tecnico/detalle_asignacion.html', {'asignacion': asignacion})

@login_required
def lista_asignaciones(request):
    asignaciones = SolicitudServicio.objects.filter(tecnico_asignado=request.user).order_by('-fecha_solicitud')
    return render(request, 'tecnico/lista_asignaciones.html', {'asignaciones': asignaciones})

@login_required
def detalle_asignacion(request, asignacion_id):
    asignacion = get_object_or_404(SolicitudServicio, id=asignacion_id, tecnico_asignado=request.user)
    return render(request, 'tecnico/detalle_asignacion.html', {'asignacion': asignacion})

@login_required
def actualizar_estado_servicio(request, asignacion_id):
    asignacion = get_object_or_404(SolicitudServicio, id=asignacion_id, tecnico_asignado=request.user)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['pendiente', 'en_proceso', 'completado', 'cancelado']:
            asignacion.estado = nuevo_estado
            asignacion.save()
            messages.success(request, f'El estado de la asignación #{asignacion.id} ha sido actualizado a {nuevo_estado}.')
            return redirect('servicios:detalle_asignacion', asignacion_id=asignacion_id)
        else:
            messages.error(request, 'Estado inválido.')
            return redirect('servicios:detalle_asignacion', asignacion_id=asignacion_id)
    else:
        # Si alguien intenta acceder a esta URL con GET, lo redirigimos al detalle de la asignación
        return redirect('servicios:detalle_asignacion', asignacion_id=asignacion_id)

def es_administrador(user):
    return user.is_staff

@login_required
@user_passes_test(es_administrador)
def lista_todas_solicitudes(request):
    solicitudes = SolicitudServicio.objects.all().order_by('-fecha_solicitud')
    return render(request, 'administrador/lista_solicitudes.html', {'solicitudes': solicitudes})

@login_required
@user_passes_test(es_administrador)
def asignar_tecnico(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudServicio, id=solicitud_id)
    if request.method == 'POST':
        form = AsignarTecnicoForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            messages.success(request, f'Técnico asignado a la solicitud #{solicitud.id}.')
            return redirect('servicios:lista_todas_solicitudes')
        else:
            messages.error(request, 'Hubo un error al asignar el técnico.')
    else:
        form = AsignarTecnicoForm(instance=solicitud)
    return render(request, 'administrador/asignar_tecnico.html', {'form': form, 'solicitud': solicitud})

@login_required
@user_passes_test(es_administrador)
def detalle_solicitud_admin(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudServicio, id=solicitud_id)
    return render(request, 'administrador/detalle_solicitud.html', {'solicitud': solicitud})

def es_administrador(user):
    return user.is_staff

@login_required
@user_passes_test(es_administrador)
def lista_tipos_servicio(request):
    tipos_servicio = TipoServicio.objects.all()
    return render(request, 'administrador/lista_tipos_servicio.html', {'tipos_servicio': tipos_servicio})

@login_required
@user_passes_test(es_administrador)
def crear_tipo_servicio(request):
    if request.method == 'POST':
        form = TipoServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de servicio creado exitosamente.')
            return redirect('servicios:lista_tipos_servicio')
        else:
            messages.error(request, 'Hubo un error al crear el tipo de servicio.')
    else:
        form = TipoServicioForm()
    return render(request, 'administrador/crear_tipo_servicio.html', {'form': form})

@login_required
@user_passes_test(es_administrador)
def editar_tipo_servicio(request, tipo_id):
    tipo_servicio = get_object_or_404(TipoServicio, id=tipo_id)
    if request.method == 'POST':
        form = EditarTipoServicioForm(request.POST, instance=tipo_servicio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de servicio actualizado exitosamente.')
            return redirect('servicios:lista_tipos_servicio')
        else:
            messages.error(request, 'Hubo un error al actualizar el tipo de servicio.')
    else:
        form = EditarTipoServicioForm(instance=tipo_servicio)
    return render(request, 'administrador/editar_tipo_servicio.html', {'form': form, 'tipo_servicio': tipo_servicio})

@login_required
@user_passes_test(es_administrador)
def eliminar_tipo_servicio(request, tipo_id):
    tipo_servicio = get_object_or_404(TipoServicio, id=tipo_id)
    if request.method == 'POST':
        tipo_servicio.delete()
        messages.success(request, 'Tipo de servicio eliminado exitosamente.')
        return redirect('servicios:lista_tipos_servicio')
    return render(request, 'administrador/eliminar_tipo_servicio.html', {'tipo_servicio': tipo_servicio})

@login_required
def calificar_servicio(request, solicitud_id):
    solicitud = get_object_or_404(
        SolicitudServicio,
        id=solicitud_id,
        cliente=request.user,
        estado='completado'
    )
    try:
        calificacion_existente = CalificacionServicio.objects.get(solicitud=solicitud)
        messages.info(request, 'Ya has calificado este servicio.')
        return redirect('servicios:detalle_solicitud', solicitud_id=solicitud_id)
    except CalificacionServicio.DoesNotExist:
        if request.method == 'POST':
            form = CalificarServicioForm(request.POST)
            if form.is_valid():
                calificacion = form.save(commit=False)
                calificacion.solicitud = solicitud
                calificacion.cliente = request.user
                calificacion.save()
                messages.success(request, 'Gracias por calificar el servicio.')
                return redirect('servicios:detalle_solicitud', solicitud_id=solicitud_id)
            else:
                messages.error(request, 'Hubo un error al guardar tu calificación.')
        else:
            form = CalificarServicioForm()
        return render(request, 'cliente/calificar_servicio.html', {'form': form, 'solicitud': solicitud})
    
@login_required
def historial_servicios(request):
    solicitudes = SolicitudServicio.objects.filter(cliente=request.user, estado='completado').order_by('-fecha_solicitud')
    return render(request, 'cliente/historial_servicios.html', {'solicitudes': solicitudes})

@login_required
def solicitar_servicio(request):
    if request.method == 'POST':
        form = SolicitarServicioForm(request.POST)
        if form.is_valid():
            tipo_servicio = form.cleaned_data['tipo_servicio']
            descripcion = form.cleaned_data['descripcion']
            direccion = form.cleaned_data['direccion']
            fecha_preferida = form.cleaned_data['fecha_preferida']

            solicitud = SolicitudServicio(
                cliente=request.user,
                tipo_servicio=tipo_servicio,
                descripcion=descripcion,
                direccion=direccion,
                fecha_preferida=fecha_preferida
            )
            solicitud.save()

            # Crear notificación para el cliente
            mensaje = f'Tu solicitud de servicio para {tipo_servicio.nombre} ha sido recibida.'
            Notificacion.objects.create(usuario=request.user, mensaje=mensaje, tipo='nueva_solicitud', objeto_id=solicitud.id)

            messages.success(request, 'Tu solicitud de servicio ha sido enviada correctamente.')
            return redirect('servicios:lista_solicitudes')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = SolicitarServicioForm()
    return render(request, 'cliente/solicitar_servicio.html', {'form': form})

@login_required
def lista_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'cliente/notificaciones.html', {'notificaciones': notificaciones})

@login_required
def marcar_leida(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    if notificacion.leida:
        messages.info(request, 'Esta notificación ya ha sido marcada como leída.')
    else:
        notificacion.leida = True
        notificacion.save()
        messages.success(request, 'Notificación marcada como leída.')
    return redirect('servicios:lista_notificaciones')

def listar_servicios(request):
    tipos_servicio = TipoServicio.objects.all()
    return render(request, 'servicios/listar_servicios.html', {'tipos_servicio': tipos_servicio})
def listar_servicios(request):
    tipos_servicio = TipoServicio.objects.all()
    return render(request, 'servicios/listar_servicios.html', {'tipos_servicio': tipos_servicio})

@login_required
def ver_perfil_tecnico(request):
    try:
        perfil = request.user.perfil_tecnico
    except PerfilTecnico.DoesNotExist:
        perfil = None
    return render(request, 'tecnico/ver_perfil_tecnico.html', {'perfil': perfil})

@login_required
def editar_perfil_tecnico(request):
    try:
        perfil = request.user.perfil_tecnico
    except PerfilTecnico.DoesNotExist:
        perfil = None

    if request.method == 'POST':
        form = PerfilTecnicoForm(request.POST, instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('servicios:ver_perfil_tecnico')
        else:
            messages.error(request, 'Hubo un error al actualizar tu perfil.')
    else:
        form = PerfilTecnicoForm(instance=perfil)

    return render(request, 'tecnico/editar_perfil_tecnico.html', {'form': form})

def es_administrador(user):
    return user.is_staff  

@login_required
@user_passes_test(es_administrador)
def lista_tecnicos(request):
    try:
        grupo_tecnicos = Group.objects.get(name='Tecnicos')
        tecnicos = User.objects.filter(groups=grupo_tecnicos).prefetch_related('perfil_tecnico')
    except Group.DoesNotExist:
        tecnicos = User.objects.none()  

    return render(request, 'administrador/lista_tecnicos.html', {'tecnicos': tecnicos})

def es_administrador(user):
    return user.is_staff  

@login_required
@user_passes_test(es_administrador)
def lista_solicitudes_admin(request):
    solicitudes = SolicitudServicio.objects.all()
    return render(request, 'administrador/lista_solicitudes_admin.html', {'solicitudes': solicitudes})

def es_administrador(user):
    return user.is_staff  

@login_required
@user_passes_test(es_administrador)
def gestion_tipos_servicio(request):
    tipos_servicio = TipoServicio.objects.all()
    return render(request, 'administrador/gestion_tipos_servicio.html', {'tipos_servicio': tipos_servicio})

def pagina_principal(request):
    tipos_servicio_populares = TipoServicio.objects.all()[:3]
    return render(request, 'servicios/pagina_principal.html', {'tipos_servicio_populares': tipos_servicio_populares})

@login_required
@user_passes_test(es_administrador)
def detalle_tecnico(request, tecnico_id):
    tecnico = get_object_or_404(User, id=tecnico_id)
    try:
        perfil = tecnico.perfil_tecnico
    except PerfilTecnico.DoesNotExist:
        perfil = None
    return render(request, 'administrador/detalle_tecnico.html', {'tecnico': tecnico, 'perfil': perfil})

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'groups', 'user_permissions')

class TecnicoCreationForm(CustomUserCreationForm):
    especialidades = forms.CharField(max_length=255, required=False)
    experiencia = forms.CharField(widget=forms.Textarea, required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            perfil_tecnico = PerfilTecnico.objects.create(
                usuario=user,
                especialidades=self.cleaned_data['especialidades'],
                experiencia=self.cleaned_data['experiencia'],
                descripcion=self.cleaned_data['descripcion']
            )
        return user

class TecnicoChangeForm(CustomUserChangeForm):
    especialidades = forms.CharField(max_length=255, required=False)
    experiencia = forms.CharField(widget=forms.Textarea, required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)

    class Meta(CustomUserChangeForm.Meta):
        fields = CustomUserChangeForm.Meta.fields + ('especialidades', 'experiencia', 'descripcion')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            perfil, created = PerfilTecnico.objects.get_or_create(usuario=user)
            perfil.especialidades = self.cleaned_data['especialidades']
            perfil.experiencia = self.cleaned_data['experiencia']
            perfil.descripcion = self.cleaned_data['descripcion']
            perfil.save()
        return user
    
@login_required
@user_passes_test(es_administrador)
def lista_usuarios(request):
    usuarios = User.objects.all().order_by('username')
    grupos = Group.objects.all()
    rol_seleccionado = request.GET.get('rol')

    if rol_seleccionado:
        if rol_seleccionado == 'administrador':
            usuarios = usuarios.filter(is_staff=True)
        elif rol_seleccionado == 'tecnico':
            try:
                grupo_tecnicos = Group.objects.get(name='Tecnicos')
                usuarios = usuarios.filter(groups=grupo_tecnicos)
            except Group.DoesNotExist:
                usuarios = User.objects.none()
        elif rol_seleccionado == 'cliente':
            # Asumimos que los clientes no pertenecen al grupo 'Tecnicos' ni son staff
            usuarios = usuarios.exclude(is_staff=True).exclude(groups__name='Tecnicos')

    return render(request, 'administrador/lista_usuarios.html', {'usuarios': usuarios, 'grupos': grupos, 'rol_seleccionado': rol_seleccionado})

@login_required
@user_passes_test(es_administrador)
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('servicios:lista_usuarios')  # Redirigir a la lista de usuarios
    else:
        form = CustomUserCreationForm()
    return render(request, 'administrador/crear_usuario.html', {'form': form})

@login_required
@user_passes_test(es_administrador)
def crear_tecnico(request):
    if request.method == 'POST':
        form = TecnicoCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo_tecnicos = Group.objects.get(name='Tecnicos')
            user.groups.add(grupo_tecnicos)
            return redirect('servicios:lista_usuarios')  # Redirigir a la lista de usuarios
    else:
        form = TecnicoCreationForm()
    return render(request, 'administrador/crear_tecnico.html', {'form': form})

@login_required
@user_passes_test(es_administrador)
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('servicios:lista_usuarios')
    else:
        form = CustomUserChangeForm(instance=usuario)
    return render(request, 'administrador/editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
@user_passes_test(es_administrador)
def editar_tecnico(request, usuario_id):
    tecnico = get_object_or_404(User, id=usuario_id)
    try:
        perfil_tecnico = tecnico.perfil_tecnico
    except PerfilTecnico.DoesNotExist:
        perfil_tecnico = None

    if request.method == 'POST':
        form = TecnicoChangeForm(request.POST, instance=tecnico)
        if form.is_valid():
            form.save()
            return redirect('servicios:lista_usuarios')
    else:
        form = TecnicoChangeForm(instance=tecnico)

    return render(request, 'administrador/editar_tecnico.html', {'form': form, 'tecnico': tecnico})
@login_required
@user_passes_test(es_administrador)
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, f'El usuario "{usuario.username}" ha sido eliminado correctamente.')
        return redirect('servicios:lista_usuarios')
    else:
        return render(request, 'administrador/confirmar_eliminar_usuario.html', {'usuario': usuario})
    
@login_required
@user_passes_test(es_administrador)
def lista_grupos(request):
    grupos = Group.objects.all().order_by('name')
    return render(request, 'administrador/lista_grupos.html', {'grupos': grupos})

@login_required
@user_passes_test(es_administrador)
def crear_grupo(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'El grupo "{form.cleaned_data["name"]}" ha sido creado correctamente.')
            return redirect('servicios:lista_grupos')
    else:
        form = GroupForm()
    return render(request, 'administrador/crear_grupo.html', {'form': form})

@login_required
@user_passes_test(es_administrador)
def editar_grupo(request, grupo_id):
    grupo = get_object_or_404(Group, id=grupo_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, f'El grupo "{form.cleaned_data["name"]}" ha sido actualizado correctamente.')
            return redirect('servicios:lista_grupos')
    else:
        form = GroupForm(instance=grupo)
    return render(request, 'administrador/editar_grupo.html', {'form': form, 'grupo': grupo})

@login_required
@user_passes_test(es_administrador)
def eliminar_grupo(request, grupo_id):
    grupo = get_object_or_404(Group, id=grupo_id)
    if request.method == 'POST':
        try:
            grupo.delete()
            messages.success(request, f'El grupo "{grupo.name}" ha sido eliminado correctamente.')
            return redirect('servicios:lista_grupos')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el grupo "{grupo.name}". Puede que esté en uso.')
            return redirect('servicios:lista_grupos')
    else:
        return render(request, 'administrador/confirmar_eliminar_grupo.html', {'grupo': grupo})
    

@login_required
@user_passes_test(es_administrador)
def editar_grupo(request, grupo_id):
    grupo = get_object_or_404(Group, id=grupo_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, f'El grupo "{form.cleaned_data["name"]}" ha sido actualizado correctamente.')
            return redirect('servicios:lista_grupos')
    else:
        form = GroupForm(instance=grupo)
    return render(request, 'administrador/editar_grupo.html', {'form': form, 'grupo': grupo})

@login_required
@user_passes_test(es_administrador)
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'La información del usuario "{usuario.username}" ha sido actualizada correctamente.')
            return redirect('servicios:lista_usuarios')
    else:
        form = CustomUserChangeForm(instance=usuario)
    return render(request, 'administrador/editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
@user_passes_test(es_administrador)
def editar_tecnico(request, usuario_id):
    tecnico = get_object_or_404(User, id=usuario_id)
    try:
        perfil_tecnico = tecnico.perfil_tecnico
    except tecnico.perfil_tecnico.DoesNotExist:
        perfil_tecnico = None

    if request.method == 'POST':
        form = TecnicoChangeForm(request.POST, instance=tecnico)
        if form.is_valid():
            form.save()
            messages.success(request, f'La información del técnico "{tecnico.username}" ha sido actualizada correctamente.')
            return redirect('servicios:lista_usuarios')
    else:
        form = TecnicoChangeForm(instance=tecnico)

    return render(request, 'administrador/editar_tecnico.html', {'form': form, 'tecnico': tecnico})

def solicitar_servicio(request):
    tipo_servicio = request.GET.get('tipo')
    form = SolicitarServicioForm(initial={'tipo_servicio': tipo_servicio})
    context = {'form': form, 'tipo_servicio_seleccionado': tipo_servicio}
    return render(request, 'cliente/solicitar_servicio.html', context)

def listar_servicios(request):
    tipos_servicio = TipoServicio.objects.all() 
    return render(request, 'servicios/listar_servicios.html', {'tipos_servicio': tipos_servicio})

def solicitar_servicio(request):
    tipo_servicio = request.GET.get('tipo')
    form = SolicitarServicioForm(initial={'tipo_servicio': tipo_servicio})
    context = {'form': form, 'tipo_servicio_seleccionado': tipo_servicio}
    return render(request, 'cliente/solicitar_servicio.html', context) 

def solicitar_plomeria(request):
    form = SolicitarServicioForm(initial={'tipo_servicio': 'plomeria'})
    context = {'form': form, 'tipo_servicio_seleccionado': 'plomeria'}
    return render(request, 'cliente/solicitar_servicio.html', context) 

def solicitar_electricista(request):
    form = SolicitarServicioForm(initial={'tipo_servicio': 'electricista'})
    context = {'form': form, 'tipo_servicio_seleccionado': 'electricista'}
    return render(request, 'cliente/solicitar_servicio.html', context)

def solicitar_limpieza(request):
    form = SolicitarServicioForm(initial={'tipo_servicio': 'limpieza'})
    context = {'form': form, 'tipo_servicio_seleccionado': 'limpieza'}
    return render(request, 'cliente/solicitar_servicio.html', context) 

def lista_servicios(request):
    
    return render(request, 'servicios/lista_servicios.html')

@login_required
def solicitar_servicio(request):
    if request.method == 'POST':
        form = SolicitudServicioForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            print(f"Usuario en la solicitud: {request.user}")  # Añade esta línea
            solicitud.usuario = request.user
            solicitud.save()
            messages.success(request, '¡Tu solicitud de servicio ha sido enviada!')
            return redirect('pagina_principal')
        else:
            return render(request, 'servicios/solicitar_servicio.html', {'form': form})
    else:
        form = SolicitudServicioForm()
    return render(request, 'servicios/solicitar_servicio.html', {'form': form})

class ServicioList(generics.ListAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class SolicitudServicioCreate(generics.CreateAPIView):
    queryset = SolicitudServicio.objects.all()
    serializer_class = SolicitudServicioSerializer
    authentication_classes = [TokenAuthentication]  # Requiere autenticación por token
    permission_classes = [IsAuthenticated]  # Requiere que el usuario esté autenticado