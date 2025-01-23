from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
import os
if os.path.isfile('env.py'):
    import env

# Add these debug print statements
print("\nEnvironment Configuration:")
print("- Current working directory:", os.getcwd())
print("- Checking for env.py...")
if os.path.isfile("env.py"):
    print("- env.py loaded successfully")
else:
    print("- env.py not found")

# Add these to verify environment variables
print("- Database URL exists:", bool(os.environ.get('DATABASE_URL')))
print("- Secret Key exists:", bool(os.environ.get('SECRET_KEY')))

SECRET_KEY = os.environ.get("SECRET_KEY") or 'django-insecure-l^g7)-e&8ohk%nv$o@b=&a7+u_6yymc0thh0u7=5q4q=#32_@s'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.environ.get('DEBUG', 'False') == 'True' 
DEBUG = True
ALLOWED_HOSTS = ['8000-nikoatillio-trustedlodg-dm2l7gobngp.ws.codeinstitute-ide.net', 'localhost', '.herokuapp.com', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://*.8000-nikoatillio-trustedlodg-dm2l7gobngp.ws.codeinstitute-ide.net']

# Application definition
INSTALLED_APPS = [
    # Custom apps first
    'accounts',  # This must come before admin
    'hello_world',
    'searches',

    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_summernote',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

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
    'allauth.account.middleware.AccountMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = 'optional'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # or 'optional' or 'none'
LOGIN_REDIRECT_URL = '/accounts/edit_profile/'  # Redirect to profile setup after log in
ACCOUNT_SIGNUP_REDIRECT_URL = '/accounts/edit_profile/'
LOGIN_URL = '/accounts/login/'

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


# Database Configuration
if 'DATABASE_URL' in os.environ:
    # Production database (PostgreSQL)
    try:
        DATABASES = {
            'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
        }
        print("PostgreSQL database connected successfully")
    except Exception as e:
        print(f"PostgreSQL connection error: {e}")
        # Fallback to SQLite if PostgreSQL connection fails
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
        print("Fallback to SQLite database")
else:
    # Development database (SQLite3)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("Development mode: SQLite database in use")

# Add this after your database configuration to help debug
if DEBUG:
    print(f"\nCurrent database engine: {DATABASES['default']['ENGINE']}")

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

# Add the media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Add Summernote configuration
SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': '100%',
        'height': '480',
    },
}

# Update ACCOUNT_FORMS
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',
}

ACCOUNT_EMAIL_VERIFICATION = 'none'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Static Files (CSS, JavaScript, Images)
STATIC_URL = '/static/'  # URL to access static files in the browser

# Directory where static files are collected (when running collectstatic)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional directories where static files are stored
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Custom static files directory
]

if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'