from .base import *
import environ # Cargamos lectura de .ENV

# Si verifica esta expreion, estamos en entornode desarrollo
env = environ.Env()
environ.Env.read_env() # Lee el archivo .env automaticamente
# Cargamos las variables de entorno desde el archivo .env

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