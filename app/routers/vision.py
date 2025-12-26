from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.azure_vision_service import AzureVisionService

router = APIRouter(prefix="/vision", tags=["Clinical Vision"])
vision_service = AzureVisionService()

@router.post("/analyze-live")
async def analyze_live(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are supported")

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image file")

    try:
        analysis = vision_service.analyze_clinical_image(image_bytes)
        return {
            "status": "Analysis Complete",
            "analysis": analysis
        }
    except Exception as e:
        # 🔥 SHOW REAL ERROR TO CLIENT
        raise HTTPException(status_code=500, detail=str(e))
