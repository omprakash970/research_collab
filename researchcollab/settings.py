"""
Django settings for researchcollab project.

- In production (Render), all sensitive values come from environment variables.
- Locally, fallback defaults are used so the app runs without any env setup.

Docs: https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path

import dj_database_url

# ──────────────────────────────────────────────
# Base directory — all paths are relative to this
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent


# ──────────────────────────────────────────────
# Security
# ──────────────────────────────────────────────

# In production Render sets SECRET_KEY as an env var.
# Locally the fallback insecure key is used (fine for dev only).
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-h^2qifj9hvqtkn8%#b%pjez+kzvl3iiu94c=w)rf$76-f&be(q',
)

# Set DEBUG=False on Render via env var. Locally defaults to True.
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

# Render provides the RENDER_EXTERNAL_HOSTNAME env var.
# Accept that hostname + localhost for local dev.
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# CSRF trusted origins for Render
CSRF_TRUSTED_ORIGINS = []
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')


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
    'whitenoise.middleware.WhiteNoiseMiddleware',        # Serve static files in production
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
#
# On Render: set DATABASE_URL env var (auto-provided when you link a DB).
# Locally: falls back to your local PostgreSQL instance.
# ──────────────────────────────────────────────

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:Nancy123abc%40@localhost:5432/researchcollab_db',
        conn_max_age=600,
    )
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

STATIC_URL = '/static/'

# Directory where `collectstatic` gathers all static files for production.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise compressed & cached static file storage for production.
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}


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

