from .base import *


# Si verifica esta expreion, estamos en entornode desarrollo
secret = {
    "SECRET_KEY": os.environ.get('SECRET_KEY', 'default-secret-key'),
    "DB_NAME": os.environ.get('DB_NAME'),
    "DB_USER": os.environ.get('DB_USER'),
    "DB_PASSWORD": os.environ.get('DB_PASSWORD'),
    "DB_HOST": os.environ.get('DB_HOST'),
    "DB_PORT": os.environ.get('DB_PORT'),
}

# Printeamos para ver que que variables obtuvimos
print(secret)

DEBUG = False
ALLOWED_HOSTS = ['yourdominion.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  
        'NAME': secret.get('DB_NAME'),
        'USER': secret.get('DB_USER'),
        'PASSWORD': secret.get('DB_PASSWORD'),
        'HOST': secret.get('DB_HOST'),
        'PORT': secret.get('DB_PORT'),
    }
}

# Method for get secret_key
def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except KeyError:
        raise ImproperlyConfigured("Set the {} environment variable".format(secret_name))

SECRET_KEY = get_secret('SECRET_KEY')