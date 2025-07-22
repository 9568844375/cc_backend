# === FILE: routes/teacher.py ===
from fastapi import APIRouter, Depends
from utils.role_checker import role_required

router = APIRouter(prefix="/teacher")

@router.get("/dashboard")
def teacher_dashboard(user=Depends(role_required("teacher"))):
    return {
        "message": f"Welcome to the Teacher Dashboard, {user['full_name']}!",
        "role": user["role"],
        "email": user["email"]
    }

# 🚀 Add more teacher-specific routes here
# Example: View student applications, post collaboration requests, etc.
