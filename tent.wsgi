from tent import create_app
import logging


logging.basicConfig(stream=sys.stderr)
project_path = "/var/www/tent"
sys.path.insert(0, project_path)


application = create_app()