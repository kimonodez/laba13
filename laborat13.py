from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]

users_collection = db["users"]
posts_collection = db["posts"]
comments_collection = db["comments"]

class UserProfile(BaseModel):
    full_name: str
    age: int
    bio: str

class User(BaseModel):
    username: str
    email: str
    profile: UserProfile

@app.post("/users/")
async def create_user(user: User):
    user_id = users_collection.insert_one(user.dict(by_alias=True)).inserted_id
    return {"user_id": str(user_id)}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = users_collection.find_one({"_id": user_id})
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}/profile")
async def update_user_profile(user_id: str, profile: UserProfile):
    result = users_collection.update_one({"_id": user_id}, {"$set": {"profile": profile.dict(by_alias=True)}})
    if result.modified_count == 1:
        return {"message": "User profile updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}/profile")
async def delete_user_profile(user_id: str):
    result = users_collection.update_one({"_id": user_id}, {"$unset": {"profile": ""}})
    if result.modified_count == 1:
        return {"message": "User profile deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
