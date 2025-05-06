from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.contrib import messages
from .forms import LoginForm, RegistroUsuarioForm, PasswordResetRequestForm, SetNewPasswordForm  # Importa los nuevos formularios
from .forms import LoginForm, RegistroUsuarioForm, PasswordResetRequestForm, SetNewPasswordForm, UserProfileForm # Importa el nuevo formulario
from django.contrib.auth.decorators import login_required

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                subject = 'Restablecimiento de contraseña'
                message = render_to_string('usuarios/password_reset_email.html', {
                    'user': user,
                    'domain': request.get_host(),
                    'uid': uidb64,
                    'token': token,
                })
                send_mail(subject, message, 'tu_email@example.com', [user.email]) # Reemplaza con tu email
                messages.success(request, 'Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'No existe ningún usuario con esa dirección de correo electrónico.')
                return render(request, 'usuarios/recuperar_password.html', {'form': form})
        else:
            return render(request, 'usuarios/recuperar_password.html', {'form': form})
    else:
        form = PasswordResetRequestForm()
    return render(request, 'usuarios/recuperar_password.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Tu contraseña ha sido restablecida exitosamente. ¡Puedes iniciar sesión ahora!')
                return redirect('login')
            else:
                return render(request, 'usuarios/password_reset_confirm.html', {'form': form})
        else:
            form = SetNewPasswordForm()
            return render(request, 'usuarios/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'El enlace de restablecimiento de contraseña no es válido. Por favor, solicita un nuevo restablecimiento.')
        return redirect('password_reset_request')

def recuperar_password(request):
    return redirect('password_reset_request') # Redirigimos a la nueva vista

def modificar_perfil(request):
    return render(request, 'usuarios/perfil.html')


@login_required
def modificar_perfil(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('perfil') # Redirige de nuevo a la página de perfil
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'usuarios/perfil.html', {'form': form})

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '¡Usuario registrado exitosamente!')
            return redirect('usuarios:registro_exitoso')  # Redirigimos a la nueva URL
        else:
            return render(request, 'usuarios/registro.html', {'form': form})
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def registro_exitoso(request):
    return render(request, 'usuarios/registro_exitoso.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pagina_principal')
            else:
                return render(request, 'usuarios/login.html', {'form': form, 'error': 'Credenciales inválidas'})
        else:
            return render(request, 'usuarios/login.html', {'form': form, 'error': 'Por favor, corrige los errores del formulario'})
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})