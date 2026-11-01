import asyncio
import sys
from pathlib import Path

# Make sure the project root can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.services.ocr_service import ocr_service


async def main():
    image_path = r"C:\Users\vasuk\Downloads\ClinOCR-Bench-v1.0\ClinOCR-Bench\scans\normal\template_1_sample_1_normal.jpg"

    print("=" * 70)
    print("MediNova OCR Smoke Test")
    print("=" * 70)
    print(f"Image: {image_path}")
    print()

    result = await ocr_service.extract_from_image(image_path)

    print(f"Success: {result.get('success')}")

    if not result.get("success"):
        print(f"Error: {result.get('error')}")
        return

    print(f"Word count: {result.get('word_count')}")
    print(f"Source type: {result.get('source_type')}")
    print()
    print("-" * 70)
    print("OCR OUTPUT")
    print("-" * 70)
    print(result.get("text", ""))
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())