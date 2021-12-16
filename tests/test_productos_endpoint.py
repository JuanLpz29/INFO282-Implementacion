def test_get_productos(client):
    response = client.get('/productos/')
    assert response.status_code == 200


def test_get_producto_id(client):
    response = client.get('/productos/1')
    assert response.status_code == 200
