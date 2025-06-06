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


def test_request_escalation():
    payload = {"content": "Need material certificate"}
    resp = client.post("/requests", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["tier"] == 1
    assert len(data["urls"]) == 1
    request_id = data["id"]

    esc = client.post(f"/requests/{request_id}/escalate")
    assert esc.status_code == 200
    url_data = esc.json()
    assert url_data["tier"] == 2

    list_resp = client.get("/requests")
    assert list_resp.status_code == 200
    list_data = list_resp.json()
    match = next(r for r in list_data if r["id"] == request_id)
    assert len(match["urls"]) == 2
