"""
WSGI config for SeedInv project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""
import os
import sys

sys.path.append('/home/mich0391/WebServer')
sys.path.append('/home/mich0391/WebServer/SeedInv')
sys.path.append('/home/mich0391/Software/anaconda3/envs/Django/lib/python3.6/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SeedInv.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()