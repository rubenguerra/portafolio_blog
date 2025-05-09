"""
WSGI config for blog_portafolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_portafolio.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'blog_portafolio.settings.Prod')

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
