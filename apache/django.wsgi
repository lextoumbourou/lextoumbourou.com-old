import os,sys

sys.path.append('/srv/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'lexandstuff.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
