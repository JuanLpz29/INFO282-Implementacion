from tent import create_app
import pytest


@pytest.fixture
def app():
    app = create_app('testing.cfg')
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def pytest_configure():
    pytest.id_venta = 0
    pytest.barcode = ''
