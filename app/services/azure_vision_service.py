import os
import asyncio
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

class AzureVisionService:
    def __init__(self):
        self.client = ImageAnalysisClient(
            endpoint=os.getenv("VISION_ENDPOINT"),
            credential=AzureKeyCredential(os.getenv("VISION_KEY"))
        )

    async def analyze_clinical_image(self, image_bytes: bytes):
        try:
            # Run blocking Azure SDK in threadpool (CRITICAL FIX)
            result = await asyncio.to_thread(
                self.client.analyze,
                image_data=image_bytes,
                visual_features=[VisualFeatures.READ, VisualFeatures.TAGS]
            )

            extracted_text = []
            confidence = None

            # SAFE OCR PARSING
            if result.read and result.read.blocks:
                for block in result.read.blocks:
                    for line in block.lines or []:
                        extracted_text.append(line.text)
                        if line.words:
                            confidence = line.words[0].confidence

            # SAFE TAG PARSING
            tags = []
            if result.tags and result.tags.list:
                tags = [tag.name for tag in result.tags.list]

            return {
                "extracted_note": " ".join(extracted_text) if extracted_text else None,
                "tags": tags,
                "confidence": confidence,
            }

        except Exception as e:
            # EXPOSE REAL ERROR (IMPORTANT)
            raise RuntimeError(f"Azure Vision failed: {str(e)}")
