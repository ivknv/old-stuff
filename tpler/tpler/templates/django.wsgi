import os, sys

p=""
if p not in sys.path:
	sys.path.append(p)
os.environ['DJANGO_SETTINGS_MODULE'] = '.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
