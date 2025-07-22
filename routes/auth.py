import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from bson import ObjectId

from database import users_collection
from models.user import UserCreate, UserLogin
from utils.password import hash_password, verify_password
from utils.jwt_helper import create_access_token
from cc_config import SECRET_KEY, ALGORITHM

router = APIRouter(tags=["Auth"])

# ✅ SIGNUP Route
@router.post("/signup")
def signup(user: UserCreate):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if users_collection.find_one({
        "$or": [
            {"email": user.email},
            {"mobile_number": user.mobile_number}
        ]
    }):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed = hash_password(user.password)
    user_data = user.dict()
    user_data["password"] = hashed
    del user_data["confirm_password"]

    inserted = users_collection.insert_one(user_data)
    user_data["_id"] = str(inserted.inserted_id)  # 👈 Convert _id to string
    user_data.pop("password")  # 👈 Remove password before returning

    token = create_access_token(
        {"sub": user_data["_id"], "role": user_data["role"]},
        expires_delta=timedelta(minutes=60)
    )

    return {
        "access_token": token,
        "user": user_data
    }

# ✅ LOGIN Route
@router.post("/login")
def login(creds: UserLogin):
    # You should search using email or mobile, not by ObjectId
    user = users_collection.find_one({
        "$or": [
            {"email": creds.identifier},
            {"mobile_number": creds.identifier}
        ]
    })

    if not user or not verify_password(creds.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expires_in_minutes = 7 * 24 * 60 if creds.remember else 60

    token = create_access_token(
        {"sub": str(user["_id"]), "role": user["role"]},
        expires_delta=timedelta(minutes=expires_in_minutes)
    )

    user.pop("password")
    user["_id"] = str(user["_id"])

    return {
        "access_token": token,
        "user": user
    }
