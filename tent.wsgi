from tent import create_app

project_path = "/var/www/tent"
sys.path.insert(0, project_path)


application = create_app()