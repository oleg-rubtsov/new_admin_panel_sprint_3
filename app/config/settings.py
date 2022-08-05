import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv() 

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True' 

ALLOWED_HOSTS = ['*'] 

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

include(
    'components/installed_apps.py',
    'components/database.py',
    'components/templates.py',
    'components/middleware.py',
    'components/auth_password_validators.py',
)

INTERNAL_IPS = ["*"]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = ['movies/locale']
