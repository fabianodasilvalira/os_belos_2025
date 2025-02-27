"""
Django settings for osbelos project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=cvza3^f+m^!yltt+_p9k6$s7xxi+hm$t(9b_=*t1&1n1(%kj9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SECURE_SSL_REDIRECT = False  # Força o redirecionamento de HTTP para HTTPS
SECURE_HSTS_SECONDS = 31536000  # Define a política HTTP Strict Transport Security (HSTS)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Inclui subdomínios na política HSTS
SECURE_HSTS_PRELOAD = True  # Preload para HSTS
SECURE_BROWSER_XSS_FILTER = True  # Habilita o filtro XSS no navegador
SECURE_CONTENT_TYPE_NOSNIFF = True  # Previne que o navegador adivinhe o tipo de conteúdo


CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https://trusted.com")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social',  # Certifique-se de que este está correto
    'rest_framework',  # Django Rest Framework
    'rest_framework_simplejwt',
    'django.contrib.sites',  # Necessário para o django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Se você estiver usando login social, adicione:
    'allauth.socialaccount.providers.google',
    'corsheaders',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Adicione essa linha
    'django.middleware.common.CommonMiddleware',  # Já deve existir
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Endereço do seu frontend local (Vite)
]


CSRF_COOKIE_SECURE = True  # Garantir que o cookie CSRF seja enviado apenas por HTTPS
CSRF_COOKIE_HTTPONLY = True  # Impedir acesso ao cookie CSRF via JavaScript
CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']


AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    # outros backends, caso necessário
)
SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Verifique se está configurado corretamente
        # ou 'rest_framework_simplejwt.authentication.JWTAuthentication' se estiver usando JWT
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}



# Configuração de expiração do token JWT
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  # Define a expiração do token de acesso
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Define a expiração do token de refresh
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

ROOT_URLCONF = 'osbelos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'osbelos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Para desenvolvimento, usando o backend de e-mail de console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Para produção, configure um serviço de envio de e-mails, como o Gmail ou SendGrid:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'seu-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'sua-senha'

DEFAULT_FROM_EMAIL = 'noreply@seusite.com'


