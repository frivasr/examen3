const loginForm = document.getElementById('login-form');
const mensajeDiv = document.getElementById('mensaje');

function mostrarMensaje(mensaje, tipo = 'info') {
    mensajeDiv.textContent = mensaje;
    mensajeDiv.className = tipo;
    mensajeDiv.classList.add('mensaje-mostrar');
    setTimeout(() => {
        mensajeDiv.classList.remove('mensaje-mostrar');
    }, 3000);
}

if (loginForm) {
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();

        console.log('Formulario de inicio de sesión enviado');

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        console.log('Nombre de usuario:', username);
        console.log('Contraseña:', password);

        // Reemplaza 'http://localhost:8000/api/token/' con la URL de tu API de Django
        fetch('http://localhost:8000/api/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username, password: password })
        })
        .then(response => {
            console.log('Respuesta del servidor:', response);
            if (!response.ok) {
                let errorMessage = 'Error al iniciar sesión: ';
                switch (response.status) {
                    case 400:
                        errorMessage += 'Datos de inicio de sesión incorrectos.';
                        break;
                    case 401:
                        errorMessage += 'No autorizado. Credenciales inválidas.';
                        break;
                    case 500:
                        errorMessage += 'Error interno del servidor. Inténtalo de nuevo más tarde.';
                        break;
                    default:
                        errorMessage += 'Error desconocido.';
                }
                throw new Error(errorMessage);
            }
            return response.json();
        })
        .then(data => {
            console.log('Respuesta de inicio de sesión (JSON):', data);
            if (data.token) {
                localStorage.setItem('mi_token', data.token);
                handleSuccessfulLogin();
            } else {
                mostrarMensaje('Inicio de sesión fallido. Token no recibido.', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarMensaje(error.message, 'error');
        });
    });
} else {
    console.warn('El formulario de inicio de sesión no se encontró');
}

function handleSuccessfulLogin() {
    window.location.href = 'solicitud.html';
}
