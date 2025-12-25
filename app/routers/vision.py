from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.azure_vision_service import AzureVisionService

router = APIRouter(prefix="/vision", tags=["Clinical Vision"])
vision_service = AzureVisionService()

@router.post("/analyze-live")
async def analyze_live(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type.")

    content = await file.read()
    analysis = vision_service.analyze_clinical_image(content)

    return {
        "status": "Analysis Complete",
        "data": analysis
    }