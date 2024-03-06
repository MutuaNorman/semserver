from pathlib import Path
import os
import environ
from urllib.parse import urlparse
from datetime import timedelta
from decouple import config

#initializing environment  variables...
env = environ.Env()
environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('APP_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG_VALUE')

ALLOWED_HOSTS = ["semserver-bocynhf46a-uc.a.run.app", "localhost", "api.sempolisher.com"]
CSRF_TRUSTED_ORIGINS = ["https://semserver-bocynhf46a-uc.a.run.app", "https://api.sempolisher.com"]
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 3rd party
    'rest_framework',
    # 'django.contrib.postgres',
    'corsheaders',
    'djoser',
    'rest_framework_simplejwt',
    'social_django',

    # local apps
    'accounts',
    'questions',
    'pesapal',
    'contacts'
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

ROOT_URLCONF = 'server.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if os.environ.get("K_REVISION", None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME':config('DB_NAME'),
            'USER':config('DB_USER'),
            'PASSWORD':config('DB_PASSWORD'),
            'HOST':config('DB_HOST'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME':"sempolisher",
            'USER':"Admin",
            'PASSWORD':"Luke&4371",
            'HOST':"127.0.0.1",
            "PORT":"5432"
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'https://storage.googleapis.com/semserver-static/static/'

STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

GS_CREDENTIALS = None

GS_BUCKET_NAME = 'semserver-static'

STATIC_ROOT = '/usr/src/app/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "accounts.CustomUser"

MEDIA_URL = 'https://storage.googleapis.com/semserver-media/'

MEDIA_BUCKET_NAME = 'semserver-media' 

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Frontend development server
    "http://127.0.0.1:5173",  # Your deployed frontend domain
    "https://pesapal.com",
    "https://sempolisher.com"
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':(
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'accounts.serializers.CustomUserSerializer',
        'user': 'accounts.serializers.CustomUserSerializer',# Replace with your user serializer
        'set_username': 'accounts.serializers.CustomUserSerializer',
    },
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE':True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION':True,
    'PASSWORD_RESET_CONFIRM_URL':'account/reset-password/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_RETYPE':True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND':True,
    'SET_USERNAME_RETYPE': True,
    'TOKEN_MODEL':None,
}

DOMAIN = "sempolisher.com"

SITE_NAME = "SemPolisher"


SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')