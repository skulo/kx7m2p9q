def test_create_sensor(client):
    response = client.post("/sensors", json={"sensor_id": "S1", "city": "Budapest"})
    assert response.status_code == 200
    assert response.json()["sensor_id"] == "S1"

def test_create_duplicate_sensor(client):
    client.post("/sensors", json={"sensor_id": "S1"})
    response = client.post("/sensors", json={"sensor_id": "S1"})
    assert response.status_code == 409

def test_add_measurement_and_query(client):
    # 1. Regisztráció
    client.post("/sensors", json={"sensor_id": "S1"})
    
    # 2. Mérések beküldése
    client.post("/sensors/S1/measurements", json={"metric": "temp", "value": 20.0})
    client.post("/sensors/S1/measurements", json={"metric": "temp", "value": 30.0})
    
    # 3. Query (átlag számítás ellenőrzése: (20+30)/2 = 25)
    response = client.get("/measurements/query?metrics=temp&sensor_ids=S1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["average"] == 25.0

def test_query_invalid_date_range(client):
    response = client.get("/measurements/query?metrics=temp&date_from=2024-02-01T00:00:00&date_to=2024-01-01T00:00:00")
    assert response.status_code == 400
    assert "date_from must be before date_to" in response.json()["detail"]
