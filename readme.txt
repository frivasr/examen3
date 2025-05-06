# Servicios del Hogar - Plataforma Web

## Descripción del Proyecto

Esta es una plataforma web desarrollada con Django para conectar usuarios que necesitan servicios del hogar con técnicos especializados. La aplicación permite a los usuarios solicitar servicios, y en el futuro, permitirá a los técnicos ver y gestionar estas solicitudes.

## Funcionalidades Implementadas

Hasta el momento, se han implementado las siguientes funcionalidades:

* **Página de Bienvenida:** Una página de inicio informativa con un diseño atractivo (utilizando Bootstrap).
* **Registro de Usuarios:** Los usuarios pueden crear nuevas cuentas en la plataforma.
* **Inicio de Sesión:** Los usuarios registrados pueden iniciar sesión de forma segura.
* **Perfil de Usuario:** Se ha extendido el modelo de usuario para incluir información de técnico.
* **Administración de Técnicos:** La interfaz de administración de Django (`/admin/`) permite a los administradores designar usuarios como técnicos.
* **Formulario de Solicitud de Servicio:** Los usuarios autenticados pueden acceder a un formulario para solicitar un nuevo servicio, especificando el tipo de servicio, descripción, dirección y fecha preferida.
* **Procesamiento de Solicitud de Servicio:** Se ha implementado la lógica en el backend para recibir y guardar las solicitudes de servicio en la base de datos (aunque actualmente presenta un problema con la base de datos Oracle).

## Tecnologías Utilizadas

* **Python:** Lenguaje de programación principal.
* **Django:** Framework web de alto nivel para Python.
* **HTML:** Lenguaje de marcado para la estructura de la página web.
* **CSS:** Lenguaje de estilos para la presentación visual (se utiliza Bootstrap para facilitar el diseño).
* **JavaScript:** Para interactividad en el frontend (si se utiliza).
* **Git:** Sistema de control de versiones.
* **Oracle:** Base de datos utilizada para la persistencia de datos.

## Configuración del Entorno

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/cran/DELTD](https://github.com/cran/DELTD)
    cd servicios_hogar
    ```

2.  **Crear y activar el entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate  # En Windows
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplicar las migraciones:**
    ```bash
    python manage.py migrate
    ```

5.  **Crear un superusuario (para acceder a la administración):**
    ```bash
    python manage.py createsuperuser
    ```

## Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver