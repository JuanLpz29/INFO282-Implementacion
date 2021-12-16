def test_get_ventas(client):
    response = client.get('/ventas/')
    assert response.status_code == 200


def test_get_venta_id(client):
    response = client.get('/ventas/1')
    assert response.status_code == 200
