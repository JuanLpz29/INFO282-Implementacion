import pytest
import random
import json

product_data = {
    "nombre": "Un producto de prueba",
    "codigoBarra": "12938456",
    "precioVenta": 1500
}


def test_post_producto(client):
    missing_field_name = "nombre"
    del product_data[missing_field_name]
    response = client.post('productos/', data=json.dumps(product_data))
    assert response.status_code == 400
    message = response.json['message']
    field = list(message.keys())[0]
    assert missing_field_name == field
