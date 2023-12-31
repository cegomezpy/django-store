"""
Django settings for Ecomerce project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from . import secure_info

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = secure_info.secret_key()
ALLOWED_HOSTS = secure_info.ALLOWED_HOSTS
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = secure_info.DEBUG

# RECAPTCHA
RECAPTCHA_PUBLIC_KEY = '6LciCcwnAAAAAPFnPvuoGSsURy_2A1ZUqJchlakD'
RECAPTCHA_PRIVATE_KEY = '6LciCcwnAAAAAIsk8UkjF4gM_8toAWSN_LG2OIFg'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Ecomerce.UserApp',
    'Ecomerce.StoreApp',
    'Ecomerce.StoreApp.DetailsApp',
    'Ecomerce.StoreApp.CartApp',
    'Ecomerce.StoreApp.CheckoutApp',
    'Ecomerce.ContactApp',
    'hcaptcha_field',
    'captcha',
    'crispy_forms',
    'crispy_bootstrap4',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Ecomerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                 os.path.join(BASE_DIR, "templates"),
                 os.path.join(BASE_DIR, "templates", "Store"),
                 os.path.join(BASE_DIR, "templates", "Events"),
                 os.path.join(BASE_DIR, "templates", "Auth"),
                 os.path.join(BASE_DIR, "templates", "Contact"),
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Ecomerce.context_processors.categorys_list',
                'Ecomerce.context_processors.search_form',
                'Ecomerce.context_processors.rating_stars',
            ],
        },
    },
]
print(TEMPLATES[0]["DIRS"])
WSGI_APPLICATION = 'Ecomerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = secure_info.databases()

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# MEDIA config
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND, EMAIL_HOST, EMAIL_USE_TLS, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = secure_info.set_email_config()

# Crispy forms config
CRISPY_ALLOWED_TEMPLATE_PACKS='bootstrap4'
CRISPY_TEMPLATE_PACK='bootstrap4'