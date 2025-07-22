# === FILE: routes/upload.py ===
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from lexie.utils.document_qa import handle_uploaded_pdf
from utils.role_checker import get_current_user

router = APIRouter()

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    user=Depends(get_current_user)  # Ensures only authenticated users can upload
):
    try:
        content = await file.read()
        result = handle_uploaded_pdf(file.filename, content)

        # Log file upload if needed, based on user["role"] or user["_id"]
        print(f"📄 File uploaded by {user['role']} - {user.get('email', 'unknown')}")

        return {"reply": result}

    except Exception as e:
        print("❌ Error in upload:", str(e))
        raise HTTPException(status_code=500, detail="File upload failed")
