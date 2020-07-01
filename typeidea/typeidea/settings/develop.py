from .base import *  #NOQA

DEBUG = True

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.sqlite3',
        'Name' : os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}