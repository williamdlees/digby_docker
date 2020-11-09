import os
import os.path
import sys
import site
from shutil import copyfile, rmtree, copytree

sys.path = ['/app'] + sys.path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
from django.core.wsgi import get_wsgi_application
os.chdir('/app/scratch')

application = get_wsgi_application()
