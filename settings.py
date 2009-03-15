import os
import secrets

PROJECT_ROOT = os.path.dirname(__file__)
PRODUCTION = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

os.sys.path.append(os.path.join(PROJECT_ROOT, 'lib'));

ADMINS = (
	('Paul Annesley', 'paul@annesley.cc'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJECT_ROOT, 'pdawebsite.sqlite3')

TIME_ZONE = 'Australia/Melbourne'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
SECRET_KEY = secrets.DJANGO_SECRET_KEY

USE_I18N = False
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	os.path.join(PROJECT_ROOT, 'blog/templates'),
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.admin',
	'blog',
)
