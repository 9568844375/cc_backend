from fastapi import APIRouter, Depends
from utils.role_checker import role_required

router = APIRouter(prefix="/student")

@router.get("/dashboard")
def student_dashboard(user=Depends(role_required("student"))):
    return {"message": f"Welcome to student dashboard, {user['full_name']}"}
