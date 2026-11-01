"""
Document Processor Service
Automatically extract medicine information, medical records, and appointment details
from uploaded documents using AI
"""

import json
import logging
import re
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
import time

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Intelligent document processing service that extracts structured information
    from medical documents, prescriptions, and reports.
    """

    def __init__(self):
        self._gemini_client = None

    async def _retry_with_backoff(self, func, max_retries=3, initial_delay=2):
        """
        Retry a function with exponential backoff for 503 errors
        
        Args:
            func: Async function to retry
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds (doubles each retry)
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                return await func()
            except Exception as e:
                last_error = e
                error_msg = str(e)
                
                # Only retry on 503 (server overload) errors
                if "503" in error_msg or "UNAVAILABLE" in error_msg:
                    if attempt < max_retries - 1:
                        delay = initial_delay * (2 ** attempt)  # Exponential backoff
                        logger.warning(f"Gemini API 503 error. Retrying in {delay}s... (attempt {attempt + 1}/{max_retries})")
                        await asyncio.sleep(delay)
                        continue
                    else:
                        logger.error(f"Gemini API still unavailable after {max_retries} attempts")
                        raise RuntimeError(
                            f"Gemini API experiencing high demand. Please try again in a few minutes. "
                            f"This is a temporary Google server issue, not a problem with your upload."
                        )
                else:
                    # For other errors, don't retry
                    raise
        
        # If we get here, all retries failed
        raise last_error

    def _get_gemini_client(self):
        """Lazy-initialize Gemini client"""
        if self._gemini_client is not None:
            return self._gemini_client

        from app.config import settings
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not set. Cannot process documents intelligently.")

        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            self._gemini_client = client
            logger.info("Gemini client initialized for document processing")
            return self._gemini_client
        except Exception as e:
            logger.error(f"Gemini client init failed: {e}")
            raise RuntimeError(f"Gemini init failed: {e}")

    async def extract_medicine_information(self, ocr_text: str) -> Dict[str, Any]:
        """
        Extract structured medicine information from prescription or medicine photo.
        
        Returns:
            {
                "success": bool,
                "medicines": [{
                    "medicine_name": str,
                    "dosage": str,
                    "frequency": str,
                    "duration_days": int,
                    "instructions": str,
                    "meal_timing": str,  # "before_meal", "after_meal", "with_meal", "anytime"
                    "time_of_day": list,  # ["morning", "afternoon", "evening", "night"]
                    "current_quantity": int or None,
                    "confidence": str  # "high", "medium", "low"
                }],
                "prescriber_name": str or None,
                "prescription_date": str or None,
                "patient_name": str or None,
                "additional_instructions": str or None
            }
        """
        if not ocr_text or len(ocr_text.strip()) < 10:
            return {
                "success": False,
                "error": "Insufficient text extracted. Please ensure the image is clear."
            }

        try:
            client = self._get_gemini_client()
            
            prompt = f"""
You are a medical document analyzer. Extract medicine information from the following prescription or medicine label.

EXTRACTED TEXT:
{ocr_text[:6000]}

Please analyze and extract medicine information in JSON format. Return ONLY valid JSON, no markdown formatting.

Return this exact structure:
{{
  "success": true,
  "medicines": [
    {{
      "medicine_name": "exact medicine name",
      "dosage": "strength with unit (e.g., 500mg, 5ml)",
      "frequency": "how often (e.g., twice daily, every 8 hours, as needed)",
      "duration_days": number of days to take (integer, or null if not specified),
      "instructions": "detailed instructions",
      "meal_timing": "before_meal" | "after_meal" | "with_meal" | "anytime",
      "time_of_day": ["morning", "afternoon", "evening", "night"],
      "current_quantity": total pills/doses if mentioned (integer or null),
      "confidence": "high" | "medium" | "low"
    }}
  ],
  "prescriber_name": "Doctor name if found or null",
  "prescription_date": "YYYY-MM-DD format if found or null",
  "patient_name": "Patient name if found or null",
  "additional_instructions": "Any general instructions or warnings"
}}

Rules:
1. Extract ALL medicines mentioned in the document
2. Be conservative - if information is unclear, set confidence to "low" or "medium"
3. For time_of_day, infer from frequency (e.g., "twice daily" = ["morning", "evening"])
4. For duration_days, extract from phrases like "for 5 days", "10 day course"
5. meal_timing: infer from "before/after food", "with meals", etc.
6. If a field cannot be determined, use null
7. Return ONLY the JSON object, no explanation or markdown

Return valid JSON only.
"""

            # Use retry logic for API call
            async def make_api_call():
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(
                    None,
                    lambda: client.models.generate_content(
                        model="models/gemini-3.8-flash",
                        contents=prompt
                    )
                )
            
            response = await self._retry_with_backoff(make_api_call, max_retries=3, initial_delay=2)

            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = re.sub(r'^```(?:json)?\n?', '', response_text)
                response_text = re.sub(r'\n?```$', '', response_text)
            
            # Parse JSON response
            import json
            result = json.loads(response_text)
            
            # Validate and clean up the result
            if not result.get("medicines"):
                result["medicines"] = []
            
            # Clean and validate each medicine entry
            for med in result.get("medicines", []):
                # Ensure required fields exist
                if not med.get("medicine_name"):
                    continue
                
                # Set defaults for missing fields
                med.setdefault("dosage", "As prescribed")
                med.setdefault("frequency", "As directed")
                med.setdefault("duration_days", None)
                med.setdefault("instructions", "Follow doctor's advice")
                med.setdefault("meal_timing", "anytime")
                med.setdefault("time_of_day", [])
                med.setdefault("current_quantity", None)
                med.setdefault("confidence", "medium")
                
                # Validate meal_timing
                valid_meal_timings = ["before_meal", "after_meal", "with_meal", "anytime"]
                if med.get("meal_timing") not in valid_meal_timings:
                    med["meal_timing"] = "anytime"
                
                # Validate time_of_day
                valid_times = ["morning", "afternoon", "evening", "night"]
                med["time_of_day"] = [t for t in med.get("time_of_day", []) if t in valid_times]
            
            result["success"] = True
            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            return {
                "success": False,
                "error": "Failed to extract structured information. The document format may be unclear."
            }
        except RuntimeError as e:
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            logger.error(f"Document processing error: {e}")
            return {
                "success": False,
                "error": f"Failed to process document: {str(e)}"
            }

    async def extract_medical_record_information(self, ocr_text: str) -> Dict[str, Any]:
        """
        Extract structured medical record information from lab reports, test results, etc.
        
        Returns structured data that can be stored as a health record.
        """
        if not ocr_text or len(ocr_text.strip()) < 10:
            return {
                "success": False,
                "error": "Insufficient text extracted."
            }

        try:
            client = self._get_gemini_client()
            
            prompt = f"""
You are a medical document analyzer. Extract key information from this medical report.

EXTRACTED TEXT:
{ocr_text[:6000]}

Extract and return this information in JSON format (ONLY valid JSON, no markdown):

{{
  "success": true,
  "record_type": "lab_report" | "imaging" | "vitals" | "prescription" | "consultation_notes" | "vaccination" | "other",
  "report_name": "Name/title of the report",
  "test_date": "YYYY-MM-DD format or null",
  "key_findings": [
    {{
      "parameter": "test name or vital sign",
      "value": "measured value",
      "unit": "unit of measurement",
      "normal_range": "normal range if mentioned",
      "status": "normal" | "high" | "low" | "critical" | "unknown"
    }}
  ],
  "diagnosis": "Any diagnosis mentioned or null",
  "doctor_name": "Doctor name if found or null",
  "facility_name": "Hospital/lab name if found or null",
  "summary": "Brief summary of the report",
  "requires_attention": true | false
}}

Be thorough but conservative. If unsure, mark status as "unknown".
Return ONLY valid JSON.
"""

            # Use retry logic for API call
            async def make_api_call():
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(
                    None,
                    lambda: client.models.generate_content(
                        model="models/gemini-3.8-flash",
                        contents=prompt
                    )
                )
            
            response = await self._retry_with_backoff(make_api_call, max_retries=3, initial_delay=2)

            response_text = response.text.strip()
            
            # Remove markdown code blocks
            if response_text.startswith("```"):
                response_text = re.sub(r'^```(?:json)?\n?', '', response_text)
                response_text = re.sub(r'\n?```$', '', response_text)
            
            import json
            result = json.loads(response_text)
            result["success"] = True
            
            return result

        except Exception as e:
            logger.error(f"Medical record extraction error: {e}")
            return {
                "success": False,
                "error": f"Failed to extract record information: {str(e)}"
            }


# Singleton
document_processor = DocumentProcessor()
