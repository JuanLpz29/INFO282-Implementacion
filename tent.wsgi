import sys

project_path = "/var/www/tent"
sys.path.insert(0, project_path)
sys.path.append('/var/www/tent')
sys.path.append('/var/www/tent/tent')

from tent import create_app
import logging

logging.basicConfig(stream=sys.stderr)
application = create_app('/var/www/tent/instance/production.cfg')