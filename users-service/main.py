from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from typing import List
from pydantic import BaseModel
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = "users"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db[COLLECTION_NAME]


class User(BaseModel):
    name: str
    email: str
    password: str
    preferences: List[str]


class LoginRequest(BaseModel):
    email: str
    password: str


@app.get("/users", response_model=List[dict])
async def get_all_users():
    """
    Get all users from the MongoDB collection.
    """
    try:
        users = list(users_collection.find())
        for user in users:
            user["_id"] = str(user["_id"])
        return users
    except Exception as e:
        return {"error": str(e)}


@app.post("/users")
async def create_user(user: User):
    """
    Insert a new user into the MongoDB collection.
    """
    try:
        # Check if the email already exists
        if users_collection.find_one({"email": user.email}):
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )

        user_dict = user.model_dump()
        user_dict["created_at"] = datetime.now(timezone.utc)
        # Insert the user into the collection
        result = users_collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)

        return {"message": "User created successfully", "user": user_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login")
async def login(login_request: LoginRequest):
    """
    Login a user by verifying email and password.
    """
    try:
        # Find the user by email
        user = users_collection.find_one({"email": login_request.email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Compare the provided password with the stored password
        if user["password"] != login_request.password:
            raise HTTPException(status_code=401, detail="Invalid password")

        user["_id"] = str(user["_id"])
        return {"message": "Login successful", "user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
