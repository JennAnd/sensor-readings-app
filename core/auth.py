# Router that handles user registration and login with token authentication
from ninja import Router
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

router = Router()

# Creates a new user and gives them a unique token
@router.post("/register")
def register(request, username: str, password: str):
    user = User.objects.create_user(username=username, password=password)
    token, created = Token.objects.get_or_create(user=user)
    return {"token": token.key}

# Logs in user and returns their token if credentials are correct
@router.post("/token")
def login(request, username: str, password: str):
    user = authenticate(username=username, password=password)
    if not user:
        return {"error": "Invalid credentials"}
    token, created = Token.objects.get_or_create(user=user) # Gets existing token or creates one if not exist
    return {"token": token.key}
