# === FILE: routes/admin.py ===
from fastapi import APIRouter, Depends
from utils.role_checker import role_required
from database import users_collection
from bson import ObjectId

router = APIRouter(prefix="/admin")

@router.get("/dashboard")
def admin_dashboard(user=Depends(role_required("admin"))):
    return {
        "message": f"Welcome to the Admin Dashboard, {user['full_name']}!",
        "role": user["role"],
        "email": user["email"]
    }

@router.get("/all-users")
def get_all_users(user=Depends(role_required("admin"))):
    users = list(users_collection.find({}, {"password": 0}))  # hide passwords
    for u in users:
        u["_id"] = str(u["_id"])  # convert ObjectId to string
    return {"users": users}

@router.delete("/delete-user/{user_id}")
def delete_user(user_id: str, user=Depends(role_required("admin"))):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found"}
