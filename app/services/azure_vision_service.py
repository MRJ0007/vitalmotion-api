import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

class AzureVisionService:
    def __init__(self):
        # Professional standard: pull from environment variables
        self.client = ImageAnalysisClient(
            endpoint=os.getenv("VISION_ENDPOINT"),
            credential=AzureKeyCredential(os.getenv("VISION_KEY"))
        )

    def analyze_clinical_image(self, image_bytes: bytes):
        try:
            # Using ComputerVision kind for OCR and Tagging [cite: 1, 18]
            result = self.client.analyze(
                image_data=image_bytes,
                visual_features=[VisualFeatures.READ, VisualFeatures.TAGS]
            )

            extracted_text = []
            if result.read:
                for line in result.read.blocks[0].lines:
                    extracted_text.append(line.text)

            tags = [tag.name for tag in result.tags.list]
            # Get confidence from the first word of the first line
            confidence = result.read.blocks[0].lines[0].words[0].confidence if extracted_text else 0

            return {
                "extracted_note": " ".join(extracted_text),
                "tags": tags,
                "confidence": confidence
            }
        except Exception as e:
            return {"error": str(e)}