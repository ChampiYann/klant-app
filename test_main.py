from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_klanten():
    response = client.get("/klanten")
    assert response.status_code == 200

# TODO get klanten inhoudelijk


def test_create_klant():
    test_klantIn = {"tafel": 5,
                    "rekening": "650e8400-e29b-41d4-a716-446655440005"}
    response = client.post("/klant", json=test_klantIn)
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["tafel"] == test_klantIn["tafel"]
    assert response.json()["rekening"] == test_klantIn["rekening"]


def test_create_klant_bad_tafel():
    test_klantIn = {"tafel": "string",
                    "rekening": "650e8400-e29b-41d4-a716-446655440005"}
    response = client.post("/klant", json=test_klantIn)
    assert response.status_code >= 400


def test_create_klant_bad_rekening():
    test_klantIn = {"tafel": 5, "rekening": "string"}
    response = client.post("/klant", json=test_klantIn)
    assert response.status_code >= 400


def test_read_klant():
    test_klantIn = {"tafel": 5,
                    "rekening": "650e8400-e29b-41d4-a716-446655440005"}
    response = client.post("/klant", json=test_klantIn)
    klant_id = response.json()["id"]
    response = client.get("/klant/" + klant_id)
    assert response.status_code == 200
    assert response.json()["id"] == klant_id
    assert response.json()["tafel"] == test_klantIn["tafel"]
    assert response.json()["rekening"] == test_klantIn["rekening"]


def test_read_klant_bad_id():
    response = client.get("/klant/" + "string")
    assert response.status_code >= 400


def test_read_klant_nonexistant_id():
    response = client.get("/klant/" + "650e8400-4444-41d4-a716-446655440005")
    assert response.status_code == 404


def test_update_klant():
    test_klantIn = {"tafel": 5,
                    "rekening": "650e8400-e29b-41d4-a716-446655440005"}
    response = client.post("/klant", json=test_klantIn)
    assert response.json()["tafel"] == test_klantIn["tafel"]
    assert response.json()["rekening"] == test_klantIn["rekening"]
    klant_id = response.json()["id"]
    test_klantIn_update = {"tafel": 7,
                    "rekening": "650e8400-e29b-41d4-4444-446655440005"}
    response = client.put("/klant/" + klant_id, json=test_klantIn_update)
    assert response.status_code == 200
    assert response.json()["id"] == klant_id
    assert response.json()["tafel"] == test_klantIn_update["tafel"]
    assert response.json()["rekening"] == test_klantIn_update["rekening"]
    # TODO check if get returns update


def test_update_klant_bad_id():
    response = client.put("/klant/" + "string")
    assert response.status_code >= 400


def test_update_klant_nonexistant_id():
    test_klantIn_update = {"tafel": 7,
                    "rekening": "650e8400-e29b-41d4-4444-446655440005"}
    response = client.put("/klant/" + "650e8400-4444-41d4-a716-446655440005", json=test_klantIn_update)
    assert response.status_code == 404


def test_delete_klant():
    test_klantIn = {"tafel": 5,
                    "rekening": "650e8400-e29b-41d4-a716-446655440005"}
    response = client.post("/klant", json=test_klantIn)
    assert response.json()["tafel"] == test_klantIn["tafel"]
    assert response.json()["rekening"] == test_klantIn["rekening"]
    klant_id = response.json()["id"]
    response = client.delete("/klant/" + klant_id)
    assert response.status_code == 200
    assert response.json()["id"] == klant_id
    assert response.json()["tafel"] == test_klantIn["tafel"]
    assert response.json()["rekening"] == test_klantIn["rekening"]
    # TODO check if get return non existant


def test_delete_klant_bad_id():
    response = client.delete("/klant/" + "string")
    assert response.status_code >= 400


def test_delete_klant_nonexistant_id():
    response = client.delete("/klant/" + "650e8400-4444-41d4-a716-446655440005")
    assert response.status_code == 404


## TODO get per tafel