"""
OCR Service
EasyOCR + OpenCV preprocessing for medical report text extraction
"""

import logging
import os
import io
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Lazy reader — EasyOCR model loads ~1GB on first use
_reader = None


def _get_reader():
    """Lazily initialize EasyOCR reader."""
    global _reader
    if _reader is not None:
        return _reader
    try:
        import easyocr
        logger.info("Loading EasyOCR model (first time may take a minute)...")
        _reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        logger.info("EasyOCR model loaded successfully")
        return _reader
    except ImportError:
        raise RuntimeError("easyocr is not installed. Run: pip install easyocr")
    except Exception as e:
        logger.error(f"EasyOCR initialization failed: {e}")
        raise RuntimeError(f"OCR initialization failed: {e}")


class OCRService:
    """Medical document OCR service using EasyOCR with optional OpenCV preprocessing."""

    @staticmethod
    def _preprocess_image(image_bytes: bytes) -> bytes:
        """
        Apply OpenCV preprocessing to improve OCR accuracy.
        - Grayscale conversion
        - Contrast enhancement (CLAHE)
        - Gaussian denoising
        - Adaptive thresholding for binarization
        """
        img = None
        try:
            import cv2
            import numpy as np

            # Decode image
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                logger.warning("Failed to decode image, using raw bytes")
                return image_bytes

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # CLAHE for contrast enhancement
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)

            # Gaussian denoise
            denoised = cv2.GaussianBlur(enhanced, (3, 3), 0)

            # Adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                denoised, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )

            # Encode back to bytes
            _, buffer = cv2.imencode('.png', thresh)
            return buffer.tobytes()

        except Exception as e:
            logger.warning(f"OpenCV preprocessing failed (using raw image): {e}")
            return image_bytes

    async def extract_from_image(self, file_path: str) -> dict:
        """
        Extract text from an image file (JPEG, PNG, WEBP, BMP).
        Applies OpenCV preprocessing before OCR.
        """
        try:
            with open(file_path, 'rb') as f:
                image_bytes = f.read()

            # Preprocess with OpenCV
            processed_bytes = self._preprocess_image(image_bytes)

            import asyncio
            import numpy as np

            def _run_ocr():
                reader = _get_reader()
                import numpy as np
                import cv2
                
                # Decode bytes to image array
                nparr = np.frombuffer(processed_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if img is None:
                    raise ValueError("Failed to decode image for OCR")
                
                results = reader.readtext(img, detail=0, paragraph=True)
                return results

            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(None, _run_ocr)

            extracted_text = '\n'.join(results) if results else ''

            return {
                "success": True,
                "text": extracted_text,
                "word_count": len(extracted_text.split()),
                "source_type": "image",
                "file_path": file_path
            }

        except RuntimeError as e:
            return {"success": False, "error": str(e)}
        except FileNotFoundError:
            return {"success": False, "error": f"File not found: {file_path}"}
        except Exception as e:
            logger.error(f"Image OCR error: {e}")
            return {"success": False, "error": f"OCR failed: {str(e)}"}

    async def extract_from_pdf(self, file_path: str) -> dict:
        """
        Extract text from a PDF file.
        Converts each page to image, then applies OCR.
        """
        try:
            # Try direct PDF text extraction first (for text-based PDFs)
            try:
                import pypdf
                reader_pdf = pypdf.PdfReader(file_path)
                text_pages = []
                for page in reader_pdf.pages:
                    text = page.extract_text()
                    if text and text.strip():
                        text_pages.append(text.strip())

                if text_pages:
                    full_text = '\n\n'.join(text_pages)
                    if len(full_text.strip()) > 50:  # Enough text extracted
                        return {
                            "success": True,
                            "text": full_text,
                            "word_count": len(full_text.split()),
                            "source_type": "pdf_text",
                            "file_path": file_path
                        }
            except Exception:
                pass  # Fall through to image-based OCR

            # Image-based OCR for scanned PDFs
            try:
                from pdf2image import convert_from_path
            except ImportError:
                logger.warning("pdf2image not installed - PDF to image conversion unavailable")
                return {
                    "success": False,
                    "error": "PDF OCR requires additional setup. Please upload your document as an image (PNG/JPG) instead."
                }
            
            try:
                images = convert_from_path(file_path, dpi=200, fmt='png')
            except Exception as e:
                error_msg = str(e).lower()
                logger.error(f"PDF conversion failed: {e}")
                
                # Check if it's a poppler error
                if 'poppler' in error_msg or 'pdftoppm' in error_msg or 'unable to get page count' in error_msg:
                    return {
                        "success": False,
                        "error": "PDF processing requires system tools that are not installed. Please upload your document as an image (PNG/JPG/JPEG) instead, or use a text-based PDF."
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to process PDF. Please try uploading as an image (PNG/JPG) instead."
                    }

            import asyncio
            all_text = []

            for i, image in enumerate(images[:10]):  # Max 10 pages
                import io
                img_bytes = io.BytesIO()
                image.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                raw_bytes = img_bytes.read()

                processed = self._preprocess_image(raw_bytes)

                def _run_page_ocr(pb=processed):
                    reader = _get_reader()
                    import numpy as np
                    import cv2
                    
                    # Decode bytes to image array
                    nparr = np.frombuffer(pb, np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    if img is None:
                        raise ValueError("Failed to decode PDF page image for OCR")
                    
                    results = reader.readtext(img, detail=0, paragraph=True)
                    return results

                loop = asyncio.get_event_loop()
                page_results = await loop.run_in_executor(None, _run_page_ocr)
                if page_results:
                    all_text.extend(page_results)

            full_text = '\n'.join(all_text)
            return {
                "success": True,
                "text": full_text,
                "word_count": len(full_text.split()),
                "source_type": "pdf_ocr",
                "pages_processed": len(images),
                "file_path": file_path
            }

        except RuntimeError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"PDF OCR error: {e}")
            return {"success": False, "error": f"PDF OCR failed: {str(e)}"}

    async def extract_from_file(self, file_path: str, content_type: str) -> dict:
        """
        Auto-detect file type and extract text.
        Dispatches to image or PDF extractor.
        """
        if content_type == 'application/pdf':
            return await self.extract_from_pdf(file_path)
        elif content_type.startswith('image/'):
            return await self.extract_from_image(file_path)
        else:
            return {
                "success": False,
                "error": f"Unsupported file type: {content_type}. Use JPEG, PNG, or PDF."
            }


# Singleton
ocr_service = OCRService()
