"""
Django settings for researchcollab project.

This configuration is intended for **local development** only.
For production deployment, ensure DEBUG is False, SECRET_KEY is
rotated, ALLOWED_HOSTS is restricted, and database credentials
are loaded from environment variables.

Docs: https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

# ──────────────────────────────────────────────
# Base directory — all paths are relative to this
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent


# ──────────────────────────────────────────────
# Security
# ──────────────────────────────────────────────

# SECURITY WARNING: replace this key before deploying to production.
SECRET_KEY = 'django-insecure-h^2qifj9hvqtkn8%#b%pjez+kzvl3iiu94c=w)rf$76-f&be(q'

# SECURITY WARNING: never run with DEBUG = True in production.
DEBUG = True

# In production, list only your actual domain(s) here.
# 'testserver' is included for Django's test client (manage.py test).
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']


# ──────────────────────────────────────────────
# Installed applications
# ──────────────────────────────────────────────

INSTALLED_APPS = [
    # Django built-in
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps (Phase 1–4)
    'apps.accounts',          # Authentication & roles
    'apps.projects',          # Research project management
    'apps.documents',         # Document sharing & uploads
    'apps.communication',     # Project discussion threads
]


# ──────────────────────────────────────────────
# Middleware
# ──────────────────────────────────────────────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ──────────────────────────────────────────────
# URL configuration
# ──────────────────────────────────────────────

ROOT_URLCONF = 'researchcollab.urls'


# ──────────────────────────────────────────────
# Templates
# ──────────────────────────────────────────────

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ──────────────────────────────────────────────
# WSGI
# ──────────────────────────────────────────────

WSGI_APPLICATION = 'researchcollab.wsgi.application'


# ──────────────────────────────────────────────
# Database — PostgreSQL
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# ──────────────────────────────────────────────

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'researchcollab_db',        # Database name
        'USER': 'postgres',                  # PostgreSQL username
        'PASSWORD': 'Nancy123abc@',          # ← CHANGE THIS to your password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# ──────────────────────────────────────────────
# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
# ──────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ──────────────────────────────────────────────
# Internationalization
# ──────────────────────────────────────────────

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ──────────────────────────────────────────────
# Static files (CSS, JS, images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
# ──────────────────────────────────────────────

STATIC_URL = 'static/'


# ──────────────────────────────────────────────
# Media files (user-uploaded content)
# ──────────────────────────────────────────────

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ──────────────────────────────────────────────
# Primary key type
# ──────────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ──────────────────────────────────────────────
# Authentication
# ──────────────────────────────────────────────

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

