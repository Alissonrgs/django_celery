"""
Django settings for django_celery project.

Generated by 'django-admin startproject' using Django 1.11.12.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from kombu import Exchange, Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'czb$ovk3kgbapzodoxz0va)-o%*_un&ty^%n(i+s$f*nrzmz+3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Celery Worker Settings

NORMAL_EXCHANGE = Exchange('normal')
BEAT_EXCHANGE = Exchange('beat')
TRANSIENT_EXCHANGE = Exchange('transient', delivery_mode=1)

CELERY_TASK_QUEUES = [
    Queue(
        'normal',
        NORMAL_EXCHANGE,
        routing_key='normal',
        queue_arguments={'x-max-priority': 10}
    ),
    Queue(
        'beat',
        BEAT_EXCHANGE,
        routing_key='beat',
        queue_arguments={'x-max-priority': 10}
    ),
    Queue(
        'transient',
        TRANSIENT_EXCHANGE,
        routing_key='transient'
    )
]
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ACKS_LATE = True
CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
CELERY_RESULT_PERSISTENT = True
CELERY_TASK_DEFAULT_EXCHANGE = 'normal'
CELERY_TASK_DEFAULT_QUEUE = 'normal'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'normal'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_TRACK_STARTED = True


# Celery Beat Settings

CELERYBEAT_SCHEDULE = {
    'periodic-task-01': {
        'task': 'app.tasks.periodic_task_01',
        'schedule': crontab(minute='*/1')
    },
    'periodic-task-02': {
        'task': 'app.tasks.periodic_task_02',
        'schedule': crontab(minute='*/2')
    }
}


# Application definition

INSTALLED_APPS = [
    'app.apps.AppConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_celery_beat',
    'django_extensions'
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

ROOT_URLCONF = 'django_celery.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'django_celery.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
