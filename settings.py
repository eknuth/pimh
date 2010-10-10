# Django settings for portland project.

from os import path 

PROJECT_PATH = path.realpath(path.dirname(__file__))

pimh_gmaps_api_key="ABQIAAAAkUlmIW1X-La8Y_JDbMsIaBRR1j-rEcJXdOU7dBo3yykxH08DuBR2MwDjASoOuLRduHmnevD97SAKWQ"
portlandismyhomeland_gmaps_api_key="ABQIAAAAkUlmIW1X-La8Y_JDbMsIaBQdkgRPlMVKT1vD1nTRJCRPuPWGKxT4RPVCd15nQW5msLk-f0ljd7C1Eg"
#api_key="ABQIAAAAkUlmIW1X-La8Y_JDbMsIaBQdkgRPlMVKT1vD1nTRJCRPuPWGKxT4RPVCd15nQW5msLk-f0ljd7C1Eg"
yelp_api_key='TyYPaW3bfrfJC4v0RIsiaQ'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'homeland'             # Or path to database file if using sqlite3.
DATABASE_USER = 'homeland'             # Not used with sqlite3.
DATABASE_PASSWORD = 'homeland'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'US/Pacific'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

STATIC_DOC_ROOT = path.join(PROJECT_PATH, 'static')


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '11%vd34$ni--q*1#tq&ko9wqbql#4-dk&n1h$f_%m^7erufwys'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	path.join(PROJECT_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.gis',
    'homeland',
    'transit',
)