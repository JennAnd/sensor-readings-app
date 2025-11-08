import pytest
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@pytest.mark.django_db
def test_create_sensor_requires_auth(client):
    """POST /api/sensors should require authentication"""
        
    # Try to create a sensor without token
    r = client.post("/api/sensors", data={"name": "Test Sensor", "type": "Env"})
        
    # Expect 401 Unathorized
    assert r.status_code == 401


@pytest.mark.django_db
def test_create_sensor_with_auth(client):
    """POST /api/sensors should work when user is logged in"""
    # Create a user and a token
    user = User.objects.create_user(username="sensor_user", password="pw")
    token, _ = Token.objects.get_or_create(user=user)

    # Send data in JSON format with the Bearer token
    res = client.post(
        "/api/sensors",
        data=json.dumps({"name": "Living Room", "type": "Env"}),  # Send JSON data
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {token.key}",
    )

    # Should return 200 or 201 if sensor is created successfully
    assert res.status_code in (200, 201)
    data = res.json()
    assert data["name"] == "Living Room"