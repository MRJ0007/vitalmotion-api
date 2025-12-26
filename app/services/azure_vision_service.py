import os
import requests

VISION_ENDPOINT = os.getenv("VISION_ENDPOINT")
VISION_KEY = os.getenv("VISION_KEY")

class AzureVisionService:
    def analyze_clinical_image(self, image_bytes: bytes):
        if not VISION_ENDPOINT or not VISION_KEY:
            raise RuntimeError("VISION_ENDPOINT or VISION_KEY is missing")

        # Image Analysis v4 (production-safe)
        url = f"{VISION_ENDPOINT.rstrip('/')}/computervision/imageanalysis:analyze"

        params = {
            "api-version": "2023-10-01",
            "features": "read,tags",
            "language": "en"
        }

        headers = {
            "Ocp-Apim-Subscription-Key": VISION_KEY,
            "Content-Type": "application/octet-stream"
        }

        response = requests.post(
            url,
            headers=headers,
            params=params,
            data=image_bytes,
            timeout=30
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Azure Vision error {response.status_code}: {response.text}"
            )

        result = response.json()

        # ---------- SAFE PARSING ----------
        extracted_text = []
        confidence = None

        read_result = result.get("readResult", {})
        for block in read_result.get("blocks", []):
            for line in block.get("lines", []):
                extracted_text.append(line.get("text", ""))
                if line.get("words"):
                    confidence = line["words"][0].get("confidence")

        tags = [
            t.get("name")
            for t in result.get("tagsResult", {}).get("values", [])
        ]

        return {
            "extracted_note": " ".join(extracted_text) if extracted_text else None,
            "tags": tags,
            "confidence": confidence
        }
