def test_get_compras(client):
    response = client.get('/compras/')
    assert response.status_code == 200


def test_get_compra_id(client):
    response = client.get('/compras/1')
    assert response.status_code == 200
