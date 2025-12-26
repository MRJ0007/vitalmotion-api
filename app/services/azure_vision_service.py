import os
import requests
from dotenv import load_dotenv, find_dotenv

# Logic: Search for .env only if not already set (typical for production)
load_dotenv(find_dotenv())

class AzureVisionService:
    def __init__(self):
        # We don't set variables here so they can be refreshed from env if changed
        pass

    def analyze_clinical_image(self, image_bytes: bytes):
        # 1. FETCH CREDENTIALS (Works for both .env and Azure App Settings)
        endpoint = os.getenv("VISION_ENDPOINT")
        key = os.getenv("VISION_KEY")

        if not endpoint or not key:
            raise RuntimeError("Azure Vision Configuration missing (Endpoint/Key)")

        # 2. CONSTRUCT URL (v4.0 Production Safe)
        # Ensure we don't have double slashes if the endpoint ends with /
        clean_endpoint = endpoint.strip().rstrip("/")
        url = f"{clean_endpoint}/computervision/imageanalysis:analyze"

        params = {
            "api-version": "2023-10-01",
            "features": "read,tags",
            "language": "en"
        }

        headers = {
            "Ocp-Apim-Subscription-Key": key,
            "Content-Type": "application/octet-stream"
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                params=params,
                data=image_bytes,
                timeout=30
            )

            if response.status_code != 200:
                raise RuntimeError(f"Azure API Error {response.status_code}: {response.text}")

            result = response.json()

            # 3. ROBUST PARSING (v4.0 Schema)
            # In v4.0 'readResult' contains 'blocks', and blocks contain 'lines'
            extracted_text = []

            read_result = result.get("readResult", {})
            for block in read_result.get("blocks", []):
                for line in block.get("lines", []):
                    # v4.0 uses 'content' for the full string in a line
                    text_content = line.get("content", line.get("text", ""))
                    if text_content:
                        extracted_text.append(text_content)

            tags = [
                t.get("name")
                for t in result.get("tagsResult", {}).get("values", [])
            ]

            return {
                "extracted_note": " ".join(extracted_text) if extracted_text else None,
                "tags": tags,
                "model_version": result.get("modelVersion", "v4.0")
            }

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error connecting to Azure: {str(e)}")

vision_service = AzureVisionService()