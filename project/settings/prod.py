from .base import *
import environ # Cargamos lectura de .ENV
import os

# Si verifica esta expreion, estamos en entornode desarrollo
env = environ.Env()
#environ.Env.read_env() # Lee el archivo .env automaticamente
# Cargamos las variables de entorno desde el archivo .env

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# DEBUGGING: Imprimir variables obtenidas
print("🔍 Variables de entorno detectadas:")
print(f"DB_NAME: {env('DB_NAME', default='NO ENCONTRADO')}")
print(f"DB_USER: {env('DB_USER', default='NO ENCONTRADO')}")
print(f"DB_PASSWORD: {env('DB_PASSWORD', default='NO ENCONTRADO')}")
print(f"DB_HOST: {env('DB_HOST', default='NO ENCONTRADO')}")
print(f"DB_PORT: {env('DB_PORT', default='NO ENCONTRADO')}")
print(f"SECRET_KEY: {env('SECRET_KEY', default='NO ENCONTRADO')}")

# Printeamos para ver que que variables obtuvimos
#print("clave \n", secret)

DEBUG = False
ALLOWED_HOSTS = ['brava.okarol.com', 'localhost', '127.0.0.1']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

SECRET_KEY = env('SECRET_KEY')
