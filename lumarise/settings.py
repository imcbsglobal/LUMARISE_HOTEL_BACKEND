from pathlib import Path
import os
import dotenv
dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-+44^09@lx=6$oj!j8rwez)2ll@*yk)hlw5uv1tu3@_#o^*fe3r'

DEBUG = True

ALLOWED_HOSTS = ["lumarisehotel.com", "www.lumarisehotel.com", "127.0.0.1", "localhost"]


# gfhbj

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'storages',

    # Local apps
    'hotel',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lumarise.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'lumarise.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'lumarise_db',
#         'USER': 'postgres',
#         'PASSWORD': 'info@imc',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'LUMARISE_DB',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / "static"

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / "media"


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Cloudflare R2 Storage Configuration
CLOUDFLARE_R2_ENABLED = os.getenv('CLOUDFLARE_R2_ENABLED', 'false').lower() == 'true'

if CLOUDFLARE_R2_ENABLED:
    # R2 Credentials
    AWS_ACCESS_KEY_ID = os.getenv('CLOUDFLARE_R2_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('CLOUDFLARE_R2_SECRET_KEY')
    
    # R2 Configuration
    CLOUDFLARE_R2_BUCKET_NAME = os.getenv('CLOUDFLARE_R2_BUCKET')
    CLOUDFLARE_R2_ENDPOINT = os.getenv('CLOUDFLARE_R2_BUCKET_ENDPOINT')
    CLOUDFLARE_R2_PUBLIC_URL = os.getenv('CLOUDFLARE_R2_PUBLIC_URL')
    CLOUDFLARE_R2_ACCOUNT_ID = os.getenv('CLOUDFLARE_R2_ACCOUNT_ID', '')

    
    # Django 5.x STORAGES setting (replaces DEFAULT_FILE_STORAGE)
    STORAGES = {
        "default": {
            "BACKEND": "lumarise.storage.R2MediaStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    
    # Media files URL
    if CLOUDFLARE_R2_PUBLIC_URL:
        MEDIA_URL = f'{CLOUDFLARE_R2_PUBLIC_URL}/media/'
        # STATIC_URL = f'{CLOUDFLARE_R2_PUBLIC_URL}/static/'
    else:
        MEDIA_URL = f'{CLOUDFLARE_R2_ENDPOINT}/{CLOUDFLARE_R2_BUCKET_NAME}/media/'
else:
    # Local storage fallback
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    MEDIA_URL = '/media/'


# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://lumarisehotel.com",
    "https://www.lumarisehotel.com",
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "lumarisehotels@gmail.com"
EMAIL_HOST_PASSWORD = "ceqzgojnxjhqssrp"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER