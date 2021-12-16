def test_get_usuarios(client):
    response = client.get('/usuarios/')
    assert response.status_code == 200


def test_get_usuario_id(client):
    response = client.get('/usuarios/1')
    assert response.status_code == 200
