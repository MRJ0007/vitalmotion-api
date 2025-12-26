from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.azure_vision_service import vision_service
import logging

# Setup logging for production debugging
logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/vision", tags=["Clinical Vision"])

@router.post("/analyze-live")
async def analyze_live(file: UploadFile = File(...)):
    # 1. VALIDATION
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files (jpg, png) are supported")

    try:
        # 2. READ BYTES (Memory Efficient)
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Received an empty file")

        # 3. CALL SERVICE
        analysis = vision_service.analyze_clinical_image(image_bytes)

        return {
            "status": "Success",
            "filename": file.filename,
            "analysis": analysis
        }

    except RuntimeError as re:
        logger.error(f"Azure Vision logic failure: {str(re)}")
        raise HTTPException(status_code=502, detail=str(re))
    except Exception as e:
        logger.error(f"Unexpected production error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during image analysis")
    finally:
        # Always close the file to free up production memory
        await file.close()