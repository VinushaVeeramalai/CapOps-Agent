import re

def analyze_image(base64_img: str) -> dict:
    # Local heuristic placeholder to keep endpoint available offline.
    if not base64_img:
        return {"type": "OTHER", "extracted_data": {}}

    if len(base64_img) > 50000:
        return {"type": "FORM", "extracted_data": {"note": "Large image payload received"}}

    if re.search(r"[A-Za-z0-9+/=]{100,}", base64_img):
        return {"type": "OTHER", "extracted_data": {"note": "Image received; deep analysis unavailable in local mode"}}

    return {"type": "OTHER", "extracted_data": {}}
