"""
Django settings for Legacy Academy Tracking System.

Generated for Django 4.2.17 with environment-based configuration.
"""

from pathlib import Path
import os
import dj_database_url
from decouple import config, UndefinedValueError

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Allow build-time fallback for Render deployment, but require real key for runtime
try:
    SECRET_KEY = config('SECRET_KEY')
except UndefinedValueError:
    # Build-time fallback for Render deployment - not used in production runtime
    if os.environ.get('RENDER') or os.environ.get('BUILD_TIME'):
        SECRET_KEY = 'build-time-temp-key-not-for-production'
    else:
        raise UndefinedValueError('SECRET_KEY not found. Must be provided via environment variable.')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# SECURITY WARNING: Specific hosts only - no wildcard in production
# Handle Render deployment with proper host configuration
allowed_hosts_config = config('ALLOWED_HOSTS', default='localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_config.split(',')]

# Add Render domain patterns if not already specified
render_patterns = ['.onrender.com', '*.onrender.com', 'legacy-academy-tracking.onrender.com', 'legacytracker.onrender.com']
for pattern in render_patterns:
    if pattern not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(pattern)

# Add testserver for Django testing
if 'testserver' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('testserver')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    
    # Local apps
    'schools.apps.SchoolsConfig',
    'students.apps.StudentsConfig',
    'attendance.apps.AttendanceConfig',
    'visits.apps.VisitsConfig',
    'reports.apps.ReportsConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'attendance_system.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'attendance_system.wsgi.application'

# Database configuration
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Parse DATABASE_URL for Render/Heroku style deployments
    # Disable connection pooling for Render to prevent stale connections
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=0)
    }
else:
    # Attempt to configure PostgreSQL from individual environment variables
    DB_NAME_PG = config('DATABASE_NAME', default=None)
    DB_USER_PG = config('DATABASE_USER', default=None)
    DB_PASSWORD_PG = config('DATABASE_PASSWORD', default=None)
    DB_HOST_PG = config('DATABASE_HOST', default='localhost')
    DB_PORT_PG = config('DATABASE_PORT', default='5432')
    
    if DB_NAME_PG and DB_USER_PG is not None:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': DB_NAME_PG,
                'USER': DB_USER_PG,
                'PASSWORD': DB_PASSWORD_PG,
                'HOST': DB_HOST_PG,
                'PORT': DB_PORT_PG,
            }
        }
    else:
        # Fallback to SQLite for development
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lusaka'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
    
    # CSRF trusted origins for Render deployment
    csrf_trusted_origins = config('CSRF_TRUSTED_ORIGINS', default='')
    if csrf_trusted_origins:
        CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_trusted_origins.split(',')]

# Admin URL customization for security
ADMIN_URL = config('ADMIN_URL', default='admin/')

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

# CORS settings for API access
CORS_ALLOWED_ORIGINS = [
    "https://localhost:3000",
    "http://localhost:3000",
]

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'attendance_system': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Custom user model (to be created)
AUTH_USER_MODEL = 'schools.User'

# Celery configuration (for future async tasks)
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE