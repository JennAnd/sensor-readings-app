import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import Sensor, Reading
from django.utils import timezone
from datetime import timedelta

# ------------ Readings: Filter and newest first order
@pytest.mark.django_db
def test_readings_filter_and_order(client):
    """GET /api/sensors/{id}/readings should return filtered and newest first readings"""
    # Create user and token
    user = User.objects.create_user(username="readingtest", password="test1234")
    token,  _ = Token.objects.get_or_create(user=user)

    # Create sensor for this user
    sensor = Sensor.objects.create(name="TestSensor", type="Env", owner=user)

    # Create two readings with different timestamps
    now = timezone.now()
    old = Reading.objects.create(sensor=sensor, temperature=18, humidity=44, timestamp=now - timedelta(minutes=3))
    new = Reading.objects.create(sensor=sensor, temperature=24, humidity=49, timestamp=now - timedelta(minutes=1))

    # Send GET request with auth token
    res = client.get(f"/api/sensors/{sensor.id}/readings", HTTP_AUTHORIZATION=f"Bearer {token.key}")

    # Check response is ok and ordered newest first
    assert res.status_code == 200
    data = res.json()
    assert [r["id"] for r in data] == [new.id, old.id]