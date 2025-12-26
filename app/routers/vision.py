from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.azure_vision_service import AzureVisionService

router = APIRouter(prefix="/vision", tags=["Clinical Vision"])

vision_service = AzureVisionService()

@router.post("/analyze-live")
async def analyze_live(file: UploadFile = File(...)):
    # 1. Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are supported")

    try:
        # 2. Read image bytes
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Empty image file")

        # 3. Call Azure Vision (ASYNC SAFE)
        analysis = await vision_service.analyze_clinical_image(image_bytes)

        return {
            "status": "Analysis Complete",
            "analysis": analysis
        }

    except HTTPException:
        raise  # rethrow clean HTTP errors

    except Exception as e:
        # 4. Expose Vision errors clearly (VERY IMPORTANT)
        raise HTTPException(
            status_code=500,
            detail=f"Vision analysis failed: {str(e)}"
        )
