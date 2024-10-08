"""
Django settings for my_project_aegbp project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _

# Caminhos dentro do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuração para o Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dgwmasvg7',
    'API_KEY': '167432956629929',
    'API_SECRET': 'D0pObKC938vbQbaiTtQMU1AymBQ',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticCloudinaryStorage'

# URLs para arquivos de mídia e estáticos
MEDIA_URL = '/media/'  # Usado pelo Django para gerar a URL de mídia
STATIC_URL = '/static/'  # Usado pelo Django para gerar a URL estática

# Diretórios de arquivos estáticos locais (para desenvolvimento)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'my_aegbp', 'static')]

# Diretórios para arquivos de mídia e estáticos
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

# Duração da sessão em segundos (30 minutos)
SESSION_COOKIE_AGE = 1800

# Configuração para garantir que a sessão expire após o tempo de inatividade
SESSION_SAVE_EVERY_REQUEST = True

# Handlers de erro
handler404 = 'my_project_aegbp.error_handling.handle_404'
handler500 = 'my_project_aegbp.error_handling.handle_500'
handler403 = 'my_project_aegbp.error_handling.handle_permission_denied'
handler400 = 'my_project_aegbp.error_handling.handle_bad_request'

# Configuração de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'errors.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Segurança
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Política de CSP (Content Security Policy)
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", 'fonts.googleapis.com', 'cdn.jsdelivr.net')
CSP_SCRIPT_SRC = ("'self'", 'cdn.jsdelivr.net')
CSP_IMG_SRC = ("'self'", 'data:', 'cdn.jsdelivr.net')
CSP_FONT_SRC = ("'self'", 'fonts.googleapis.com', 'fonts.gstatic.com', 'cdn.jsdelivr.net')

# Admins para notificação de erros
ADMINS = [('SancaWeb Solutions', 'suporte2024beniciosanca@gmail.com')]

# Configuração de Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aegbsuporte@gmail.com'
EMAIL_HOST_PASSWORD = 'g m i m p a w g i l y x i u a n'
DEFAULT_FROM_EMAIL = 'aegbsuporte@gmail.com'

# Configuração de Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Segurança - Manter a chave secreta em produção
SECRET_KEY = 'django-insecure-2%g3miv+7l7lk+_g3&cf01ml+mp$w7n258^(jby7*--ewlus7z'

# Configurações de Debug
DEBUG = True
ALLOWED_HOSTS = []

# Backends de Autenticação
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'my_aegbp',
    'admin_interface',
    'colorfield',
    'widget_tweaks',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'haystack',
    'rest_framework',
    'corsheaders',
    'modeltranslation',
    'storages',
    'cloudinary',
    'cloudinary_storage',
]

# Configuração do Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'my_aegbp.middleware.NotificationMiddleware',
    'my_aegbp.middleware.ExceptionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'my_project_aegbp.urls'

# Configuração de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'my_aegbp.context_processors.dashboard_cards',
                'my_aegbp.context_processors.base_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_project_aegbp.wsgi.application'

# Configuração do Banco de Dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aegbp_database',
        'USER': 'aegbpbase',
        'PASSWORD': 'cPV2szHrJbxhwfinwIRqVKcjH9KLeCeS',
        'HOST': 'dpg-cqviumdds78s739kg19g-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}

# Validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'pt'
TIME_ZONE = 'Europe/Lisbon'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('pt', 'Português'),
    ('en', 'English'),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'pt'


# Tipo de campo padrão para chaves primárias
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
