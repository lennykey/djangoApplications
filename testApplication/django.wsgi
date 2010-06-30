testApplication
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

import django.core.handlers.wsgi
sys.path.append('/home/jupiter/djAngoapplications/testApplication/')

application = django.core.handlers.wsgi.WSGIHandler()


