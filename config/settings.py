from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
import os

# Add these debug print statements
print("\nEnvironment Configuration:")
print("- Current working directory:", os.getcwd())
print("- Checking for env.py...")
if os.path.isfile("env.py"):
    import env
    print("- env.py loaded successfully")
else:
    print("- env.py not found")

# Add these to verify environment variables
print("- Database URL exists:", bool(os.environ.get('DATABASE_URL')))
print("- Secret Key exists:", bool(os.environ.get('SECRET_KEY')))

SECRET_KEY = os.environ.get("SECRET_KEY") or 'django-insecure-l^g7)-e&8ohk%nv$o@b=&a7+u_6yymc0thh0u7=5q4q=#32_@s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['8000-nikoatillio-trustedlodg-dm2l7gobngp.ws.codeinstitute-ide.net', 'localhost']

CSRF_TRUSTED_ORIGINS = ['https://*.8000-nikoatillio-trustedlodg-dm2l7gobngp.ws.codeinstitute-ide.net']

# Application definition
INSTALLED_APPS = [
    # Custom apps first
    'accounts',  # This must come before admin

    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Other custom apps
    'hello_world',
    'accounts',
    'searches',

]

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'hello_world/templates'
        ],
        'APP_DIRS': True,  # This allows Django to look for templates in app directories
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# print("\nDatabase Configuration:")
# print("- Database URL exists:", bool(os.environ.get('DATABASE_URL')))
# print("- Database URL:", os.environ.get('DATABASE_URL'))

# # Add error handling for database configuration
# try:
#     DATABASES = {
#         'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
#     }
#     print("- Database configuration successful")
# except Exception as e:
#     print("- Database configuration error:", str(e))
#     raise e

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'hello_world/static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'