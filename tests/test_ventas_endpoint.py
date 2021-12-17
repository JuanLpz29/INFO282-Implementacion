import pytest


def test_get_ventas(client):
    response = client.get('/ventas/')
    assert response.status_code == 200


def test_get_venta_id(client):
    response = client.get('/ventas/1')
    assert response.status_code == 200


def test_post_venta_iniciar(client):
    response = client.post(
        f'ventas/?nombre=joselo&codigoBarra={pytest.barcode}')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    info_venta = response.json['venta']
    producto = response.json['producto']
    assert info_venta and producto
    pytest.id_venta = info_venta['idVenta']
    assert producto


def test_post_venta_update(client):
    response = client.put(
        f'ventas/{pytest.id_venta}?nombre=joselo&operation=update&codigoBarra={pytest.barcode}')
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_put_venta_cancelar(client):
    response = client.put(
        f'ventas/{pytest.id_venta}?operation=cancel&nombre=joselo')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
