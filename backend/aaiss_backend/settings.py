"""
Django settings for aaiss_backend project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from datetime import timedelta
from pathlib import Path

import environ

env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR.joinpath('.env'))

# production/development key
SECRET_KEY = env.str("SECRET_KEY", 'orlch#mu_+2-my=fo)akh_3+^j7+7tc@v*-*z^(g*%(&lih@pv')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = ['autaaiss.com', '127.0.0.1', 'localhost', "185.252.86.114"]
CSRF_TRUSTED_ORIGINS = ['https://autaaiss.com', 'https://localhost', 'https://127.0.0.1', "http://185.252.86.114"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'backend_api',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

ROOT_URLCONF = 'aaiss_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates/html/'
        ],
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
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            BASE_DIR / 'templates/html/'],
    },
]
WSGI_APPLICATION = 'aaiss_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data' / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
APPEND_SLASH = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default auth model
AUTH_USER_MODEL = 'backend_api.Account'

# media
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ORIGIN_ALLOW_ALL = True

X_API_KEY = env.str('X_API_KEY', '')
X_SANDBOX = env.str('X_SANDBOX', '')

SERVER_EMAIL = 'smtp-relay.sendinblue.com'
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', '587')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', 'aaiss.ce.2024@gmail.com')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', 'aaiss.ce.2024@gmail.com')
ENABLE_SENDING_EMAIL = env.bool('ENABLE_SENDING_EMAIL', True)

BASE_URL = env.str('BASE_URL', 'https://aaiss.ir/')

# https://docs.djangoproject.com/en/4.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#PAYWALL SETTING
PAYWALL = env.str("PAYWALL", "ZIFY")

#ZIFY
ZIFY_AUTH = env.str("ZIFY_AUTH", "")

SKYROOM_BASE_URL = env.str("SKYROOM_URL", "https://www.skyroom.online/ch/aut_ceit_ssc")
