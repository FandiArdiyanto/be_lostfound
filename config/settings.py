from pathlib import Path
from datetime import timedelta
from decouple import config, Csv
import dj_database_url
import os

# ── Base Directory ───────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security Settings ────────────────────────────────────────────────────────
SECRET_KEY    = config('SECRET_KEY', default='django-insecure-ganti-ini-di-production')
DEBUG         = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['*']

# ── Application Definition ───────────────────────────────────────────────────
INSTALLED_APPS = [
    'daphne',                               # Harus berada di paling atas
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'channels',
    # Local apps
    'cloudinary_storage',
    'cloudinary',
    'lostfound',
    'chat',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Wajib di paling atas untuk handling CORS
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Tambahan: Untuk menghandle CSS/JS Django Admin di Railway
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION  = 'config.asgi.application'   # Konfigurasi untuk Channels/WebSocket

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

# ── Database ─────────────────────────────────────────────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600
    )
}

# ── Custom User Model ────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'lostfound.User'

# ── Auth Validators ──────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# ── Localization ──────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'id-id'
TIME_ZONE     = 'Asia/Jakarta'
USE_I18N      = True
USE_TZ        = True

# ── Static & Media (Cloudinary) ───────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Tempat berkumpulnya aset statis Django Admin di server

MEDIA_URL   = '/media/'
MEDIA_ROOT  = BASE_DIR / 'media'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Mencegah crash jika variabel belum diset di panel Railway
os.environ['CLOUDINARY_URL'] = config('CLOUDINARY_URL', default='') 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Django REST Framework (DRF) ────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
}

# ── Simple JWT ────────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':  True,
    'AUTH_HEADER_TYPES':      ('Bearer',),
}

# ── CORS Configuration ────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True

# ── CSRF Trusted Origins ──────────────────────────────────────────────────────
# Wajib untuk Django 4.x+ agar tidak terblokir saat login panel admin di domain Railway
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS', 
    default='https://lostfound-production.up.railway.app,https://*.railway.app', 
    cast=Csv()
)

# ── Django Channels (WebSocket) ───────────────────────────────────────────────
REDIS_URL = config('REDIS_URL', default=None)

if REDIS_URL:
    # Otomatis aktif di Railway jika Anda menghubungkan database Redis
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [REDIS_URL],
            },
        },
    }
else:
    # Otomatis aktif saat testing di laptop (localhost)
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        }
    }
