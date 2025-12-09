"""
Django settings for notesapi project.
"""
import dj_database_url
import os
from pathlib import Path
from datetime import timedelta
import cloudinary
import certifi

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
# Security
# ----------------------------
SECRET_KEY = "django-insecure-hdzj9j($^ke+t&6c^db(w!$%h9k#-uh*=+m!)1(7+zn0nqai2n"
DEBUG = True
ALLOWED_HOSTS = ['drex-notes-api.onrender.com', 'localhost', '127.0.0.1']

# ----------------------------
# Applications
# ----------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "cloudinary_storage", # Must be above staticfiles
    "django.contrib.staticfiles",
    "cloudinary",
    "rest_framework",
    "corsheaders",
    "notes", # Your app
]

# ----------------------------
# Middleware
# ----------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware", # Top for CORS
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ----------------------------
# URL & WSGI
# ----------------------------
ROOT_URLCONF = "notesapi.urls"
WSGI_APPLICATION = "notesapi.wsgi.application"

# ----------------------------
# Templates
# ----------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ----------------------------
# Database
# ----------------------------
# settings.py

# ...

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        # If there is no 'DATABASE_URL' in the environment (like on your laptop),
        # it falls back to this SQLite setup:
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

# ...

# ----------------------------
# Password Validation
# ----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ----------------------------
# Internationalization
# ----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ----------------------------
# Static & Media
# ----------------------------
STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ----------------------------
# Django REST Framework
# ----------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# ----------------------------
# JWT Settings
# ----------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# ----------------------------
# CORS Settings
# ----------------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# ----------------------------
# Cloudinary Config
# ----------------------------
# 1. Global Config with Certifi (Fixes WinError 10054)
cloudinary.config(
    cloud_name = 'dpst1xyto', 
    api_key = '135677568866613',       # <--- USE NEW KEY
    api_secret = 'mmH2OUCo1d6rPJT4ITqlbn91R4g', # <--- USE NEW SECRET
    secure = True,
    certificate = certifi.where() 
)

# 2. Storage Config (Fixes 401 Error)
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "dpst1xyto",
    "API_KEY": "135677568866613",       # <--- USE NEW KEY
    "API_SECRET": "mmH2OUCo1d6rPJT4ITqlbn91R4g", # <--- USE NEW SECRET
    # These settings prevent private/signed URLs
    'SECURE': True,
    'MEDIA_TAG': False,  # <--- MUST BE FALSE
    'STATIC_TAG': False, # <--- MUST BE FALSE
    'MAGIC_FILE': False, # <--- MUST BE FALSE
    'RESOURCE_TYPE': 'raw' 
}
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# 3. Storage Backends
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}