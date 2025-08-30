import os
import sys

path = '/home/justsmtp/Capstone-Project/social_media_api'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
