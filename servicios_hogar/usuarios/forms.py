# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario o Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Puedes agregar personalizaciones aquí

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, label='Nombre')
    last_name = forms.CharField(max_length=150, required=False, label='Apellido')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='Dirección de correo electrónico')

class SetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(), label='Nueva contraseña')
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirmar nueva contraseña')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')