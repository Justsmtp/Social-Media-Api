"""
WSGI config for social_media_api project.
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add project to sys.path
path = '/home/justsmtp/social_media_api'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_api.settings")

application = get_wsgi_application()
