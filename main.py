from tent import create_app
import os

_env = os.environ.get('FLASK_ENV')
if _env is None:
    _env = 'development'

application = create_app(f'{_env}.cfg')
