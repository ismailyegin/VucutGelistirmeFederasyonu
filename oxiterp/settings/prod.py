from oxiterp.settings.base import *

# Override base.py settings here


DEBUG = True
ALLOWED_HOSTS = ['sbs.tvgfbf.gov.tr']

# DATABASES = {
#   'default': {
#      'ENGINE': 'django.db.backends.postgresql',
#     'NAME': '',
#    'USER': '',
#   'PASSWORD': '',
#  'HOST': 'localhost',
# 'PORT': '5432',
# }
# }

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'kobiltek_vucutdb',
       'HOST': 'localhost',
       'PORT': '3306',
       'USER': 'vucut_root',
       'PASSWORD': 'kobil2013'
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.oracle',
#         'NAME': '',
#         'USER': 'sbs',
#         'PASSWORD': '',
#     }
# }


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join('oxiterp/static'),)
STATIC_ROOT = ''

try:
    from oxiterp.settings.local import *
except:
    pass
