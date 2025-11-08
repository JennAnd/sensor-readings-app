import pytest

# ------------ Sensor: Create sensor requires authentication
@pytest.mark.django_db
def test_create_sensor_requires_auth(client):
    """POST /api/sensors should require authentication"""
        
    # Try to create a sensor without token
    r = client.post("/api/sensors", data={"name": "Test Sensor", "type": "Env"})
        
    # Expect 401 Unathorized
    assert r.status_code == 401