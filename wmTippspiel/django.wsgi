import os
import sys

sys.path.append('/usr/lib/python2.6/site-packages/django')
sys.path.append('/home/jupiter/djangoApplications')
sys.path.append('/home/jupiter/djangoApplications/wmTippspiel')
os.environ['DJANGO_SETTINGS_MODULE'] = 'wmTippspiel.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

