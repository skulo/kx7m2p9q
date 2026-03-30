def test_create_sensor(client):
    response = client.post("/sensors", json={"sensor_id": "S1", "city": "Budapest"})
    assert response.status_code == 200
    assert response.json()["sensor_id"] == "S1"

def test_create_duplicate_sensor(client):
    client.post("/sensors", json={"sensor_id": "S1"})
    response = client.post("/sensors", json={"sensor_id": "S1"})
    assert response.status_code == 409

def test_add_measurement_and_query(client):
    # 1. Registration of sensor
    client.post("/sensors", json={"sensor_id": "S1"})
    
    # 2. Adding measurements
    client.post("/sensors/S1/measurements", json={"metric": "temp", "value": 20.0})
    client.post("/sensors/S1/measurements", json={"metric": "temp", "value": 30.0})
    
    # 3. Querying average temperature
    response = client.get("/measurements/query?metrics=temp&sensor_ids=S1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["average"] == 25.0

def test_query_invalid_date_range(client):
    response = client.get("/measurements/query?metrics=temp&date_from=2024-02-01T00:00:00&date_to=2024-01-01T00:00:00")
    assert response.status_code == 400
    assert "date_from must be before date_to" in response.json()["detail"]

def test_add_measurement_non_existent_sensor(client):
    response = client.post("/sensors/UNKNOWN/measurements", json={"metric": "temp", "value": 25.0})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_query_no_results(client):
    client.post("/sensors", json={"sensor_id": "S1"})
    # We search for a metric that has no measurements
    response = client.get("/measurements/query?metrics=pressure&sensor_ids=S1")
    assert response.status_code == 404

def test_query_multiple_metrics(client):
    client.post("/sensors", json={"sensor_id": "S1"})
    client.post("/sensors/S1/measurements", json={"metric": "temp", "value": 20.0})
    client.post("/sensors/S1/measurements", json={"metric": "hum", "value": 50.0})
    
    response = client.get("/measurements/query?metrics=temp&metrics=hum&sensor_ids=S1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # one for temp and one for hum
