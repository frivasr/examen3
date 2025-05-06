from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.contrib.auth.models import User, Group, Permission
from .models import SolicitudServicio, TipoServicio, CalificacionServicio, PerfilTecnico

class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Permisos'
    )

    class Meta:
        model = Group
        fields = ('name', 'permissions')

class SolicitarServicioForm(forms.Form):
    tipo_servicio = forms.ModelChoiceField(queryset=TipoServicio.objects.all(), label='Tipo de Servicio')
    descripcion = forms.CharField(widget=forms.Textarea, label='Descripción del Servicio')
    direccion = forms.CharField(max_length=255, label='Dirección')
    fecha_preferida = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha Preferida')

class AsignarTecnicoForm(forms.ModelForm):
    tecnico_asignado = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),  # Asume que los técnicos son staff
        required=False,
        label='Asignar Técnico'
    )

    class Meta:
        model = SolicitudServicio
        fields = ('tecnico_asignado',)

class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = ['nombre', 'descripcion']

class EditarTipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = ['nombre', 'descripcion']

class CalificarServicioForm(forms.ModelForm):
    puntuacion = forms.ChoiceField(
        choices=[(1, '1 estrella'), (2, '2 estrellas'), (3, '3 estrellas'), (4, '4 estrellas'), (5, '5 estrellas')],
        widget=forms.RadioSelect,
        label='Puntuación'
    )
    comentario = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Comentario (opcional)',
        required=False
    )

    class Meta:
        model = CalificacionServicio
        fields = ['puntuacion', 'comentario']

class PerfilTecnicoForm(forms.ModelForm):
    class Meta:
        model = PerfilTecnico
        fields = ['especialidades', 'experiencia', 'descripcion']

class CustomUserChangeForm(UserChangeForm):
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Permisos Específicos del Usuario'
    )

    class Meta(UserChangeForm.Meta):
        model = User  # Usamos el modelo User base aquí
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'groups', 'user_permissions')

class TecnicoChangeForm(CustomUserChangeForm):
    especialidades = forms.CharField(max_length=255, required=False)
    experiencia = forms.CharField(widget=forms.Textarea, required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)

    class Meta(CustomUserChangeForm.Meta):
        fields = CustomUserChangeForm.Meta.fields + ('especialidades', 'experiencia', 'descripcion')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.perfil_tecnico:
            self.fields['especialidades'].initial = self.instance.perfil_tecnico.especialidades
            self.fields['experiencia'].initial = self.instance.perfil_tecnico.experiencia
            self.fields['descripcion'].initial = self.instance.perfil_tecnico.descripcion

    def save(self, commit=True):
        user = super().save(commit=False)
        perfil, created = PerfilTecnico.objects.get_or_create(usuario=user)
        perfil.especialidades = self.cleaned_data['especialidades']
        perfil.experiencia = self.cleaned_data['experiencia']
        perfil.descripcion = self.cleaned_data['descripcion']
        if commit:
            user.save()
            perfil.save()
        return user
    
class SolicitudServicioForm(forms.ModelForm):
    fecha_preferida = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = SolicitudServicio
        fields = ['tipo_servicio', 'descripcion', 'direccion', 'fecha_preferida']

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']