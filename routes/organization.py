# === FILE: routes/organization.py ===
from fastapi import APIRouter, Depends
from utils.role_checker import role_required

router = APIRouter(prefix="/organization")

@router.get("/dashboard")
def organization_dashboard(user=Depends(role_required("organization"))):
    return {"message": f"Welcome to organization dashboard, {user['full_name']}"}
