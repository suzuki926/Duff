import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_create_and_read_product():
    payload = {
        "name": "Test Product",
        "material": "Steel",
        "manufacturing_place": "Factory A",
        "supply_chain_history": "Supplier X > Factory A",
        "recycling_info": "Recycle at Center B"
    }
    response = client.post("/products", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    product_id = data["id"]

    get_resp = client.get(f"/products/{product_id}")
    assert get_resp.status_code == 200
    read_data = get_resp.json()
    assert read_data["name"] == payload["name"]
