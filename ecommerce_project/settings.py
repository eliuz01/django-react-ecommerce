import os
from pathlib import Path
from datetime import timedelta
import socket
import dj_database_url
# ------------------------------
# BASE CONFIGURATION
# ------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
# Load SECRET_KEY from environment in production, fallback for dev
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here-change-in-production')

# Load DEBUG mode dynamically from environment (defaults to True locally)
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# ------------------------------
# ALLOWED HOSTS

# Parse ALLOWED_HOSTS from env if supplied, else fallback to local defaults
env_hosts = os.environ.get('ALLOWED_HOSTS')
if env_hosts:
    ALLOWED_HOSTS = [host.strip() for host in env_hosts.split(',') if host.strip()]
else:
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        'testserver',
        '192.168.1.*',
    ]

# Append local machine hostname for local networks
    try:
        hostname = socket.gethostname()
        ALLOWED_HOSTS.append(hostname)
    except Exception:
        pass

# ------------------------------
# INSTALLED APPS
# ------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',

    # Local apps
    'accounts',
    'products',
    'orders',
    'cart',
]

# ------------------------------
# MIDDLEWARE
# ------------------------------

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise serves static files efficiently in prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------
# URL CONFIGURATION
# ------------------------------

ROOT_URLCONF = 'ecommerce_project.urls'

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

WSGI_APPLICATION = 'ecommerce_project.wsgi.application'

# ------------------------------
# DATABASE CONFIGURATION

# Detect DATABASE_URL supplied by cloud providers (Render/Railway), otherwise fallback to individual vars
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'ecommerce_db'),
            'USER': os.environ.get('DB_USER', 'ecommerce_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'your-password'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# ------------------------------
# AUTHENTICATION CONFIGURATION
# ------------------------------

AUTH_USER_MODEL = 'accounts.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# ------------------------------
# CORS CONFIGURATION
# ------------------------------

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
]

env_cors = os.environ.get('CORS_ALLOWED_ORIGINS')
if env_cors:
    CORS_ALLOWED_ORIGINS.extend([origin.strip() for origin in env_cors.split(',') if origin.strip()])
# ------------------------------
# STATIC AND MEDIA FILES
# ------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ------------------------------
# DEFAULT SETTINGS
# ------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
