# Brava Blogs Project

<img src="static/assets/logo.jpeg" alt="Log-bravo" width="300" style="background-color:#dddcdc; padding: 10px; border-radius: 10px;">

Este es un proyecto base de **Django** diseñado para manejar el sitio web de una Radio Emisora, la idea es crear un sistema de blogs donde los usuarios brinden informacion a los clientes. Proporciona una estructura escalable y está preparado para ser utilizado con una base de datos PostgreSQL.
**ESTO ES UNA API**

---

## 🚀 Pasos de Instalación

### 1. Crear un Entorno Virtual

Utilizamos `venv` para manejar entornos virtuales. Para crear un nuevo entorno virtual llamado `env-brav`, ejecuta:

```bash
python3.11 -m venv env-brav
# o
python3 -m venv env-brav
```

Activar el entorno virtual:

- **Linux o Mac**:

```bash
source env-brav/bin/activate
```

- **Windows**:

```bash
env-brav\Scripts\activate
```

---

### 2. Instalación de Dependencias

Una vez dentro del entorno virtual, navega hasta la raíz del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

---

### 3. Configuración de Credenciales

Dentro de la raíz del proyecto, crea un archivo llamado `.env` con la siguiente estructura:

```json
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''
# Archivos de configuracion para conectar con la base de datos (DEVELOP)
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

> **Nota**: Asegúrate de cambiar los valores de `SECRET_KEY`, `DB_NAME`, `DB_USER` y `DB_PASSWORD` a los apropiados para tu configuración.

---

### 4. Configuración de la Base de Datos

Dado que utilizamos PostgreSQL como base de datos, asegúrate de tenerlo instalado y en ejecución.

---

### 5. Crear y Aplicar Migraciones

Para crear las migraciones y aplicarlas, ejecuta:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Configuración de Variables de Entorno

Configura la variable de entorno necesaria antes de ejecutar la aplicación:

- **En sistemas Unix/Linux/Mac**:

```bash
export DEVELOPMENT_ENVIRONMENT=True
```

- **En Windows (CMD)**:

```cmd
set DEVELOPMENT_ENVIRONMENT=True
```

- **En Windows (PowerShell)**:

```powershell
$env:DEVELOPMENT_ENVIRONMENT = "True"
```

---

### 7. Ejecutar el Proyecto

Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

Accede a tu proyecto desde [http://localhost:8000/](http://localhost:8000/).

---
## ¡Listo!


