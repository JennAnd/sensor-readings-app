# Router file for the core app
from ninja import Router
from .models import Sensor
from typing import List

# Create a router to handle API endpoints related to sensors
router = Router()

# Endpoint to get a list of all sensors from the database
@router.get("/sensors")
def list_sensors(request):
    sensors = Sensor.objects.all()
    return [{"id": s.id, "name": s.name, "type": s.type} for s in sensors]

