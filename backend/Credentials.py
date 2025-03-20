from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

# Initialize FastAPI
app = FastAPI()

# Enable CORS to allow communication with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Default route to check if FastAPI is running
@app.get("/")
def home():
    return {"message": "FastAPI is running"}

# Password & Username constraints
min_length = 6
password_store = []
username_store = []

class Credential(BaseModel):
    value: str

@app.post("/store-password")
def store_password(data: Credential):
    password = data.value
    if password is None or len(password) < min_length:
        raise HTTPException(status_code=400, detail="Password does not meet the required constraints.")
    
    password_store.append(password)
    return {"message": "Password stored successfully"}

@app.post("/store-username")
def store_username(data: Credential):
    username = data.value
    if username is None or len(username) < min_length:
        raise HTTPException(status_code=400, detail="Username does not meet the required constraints.")
    
    username_store.append(username)
    return {"message": "Username stored successfully"}

@app.post("/password-strength")
def calc_pass_strength(data: Credential):
    password = data.value
    if password is None or len(password) < min_length:
        raise HTTPException(status_code=400, detail="Password does not meet the required constraints.")
    
    strength = 1
    if len(password) >= 8: strength += 1
    if re.search(r'[A-Z]', password): strength += 1
    if re.search(r'[0-9]', password): strength += 1
    if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password): strength += 1

    return {"strength": min(strength, 5)}

@app.post("/username-strength")
def calc_user_strength(data: Credential):
    username = data.value
    if username is None or len(username) < min_length:
        raise HTTPException(status_code=400, detail="Username does not meet the required constraints.")
    
    strength = 1
    if len(username) >= 8: strength += 1
    if re.search(r'[A-Z]', username): strength += 1
    if re.search(r'[0-9]', username): strength += 1
    if re.search(r'[_\-.]', username): strength += 1  # Allowing underscores, hyphens, and dots

    return {"strength": min(strength, 5)}

