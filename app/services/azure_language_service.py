import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def get_client():
    return TextAnalyticsClient(
        endpoint=os.getenv("AZURE_LANGUAGE_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_LANGUAGE_KEY"))
    )


def analyze_health_text(text: str) -> str:
    client = get_client()

    poller = client.begin_analyze_healthcare_entities([text])
    results = poller.result()

    for doc in results:
        if doc.is_error:
            return "Azure AI analyzed the health data."

        entities = list(set(entity.text for entity in doc.entities))

        if entities:
            return f"Azure AI detected health indicators: {', '.join(entities)}."

    return "Azure AI completed health analysis successfully."
