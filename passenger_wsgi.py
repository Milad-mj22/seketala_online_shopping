

import sys
import os

# تنظیم مسیر پروژه
sys.path.insert(0, '/home/seketal1/seketala_online_shopping/passenger_wsgi.py')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SM.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

