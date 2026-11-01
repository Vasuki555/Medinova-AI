"""
AI Service
Google Gemini API integration using the new google.genai SDK (v2+)
Medical report analysis and conversational health assistant
"""

import logging
import asyncio
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

_client = None  # Lazy-initialized Gemini client


async def _retry_with_backoff(func, max_retries=3, initial_delay=2):
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
                        f"This is a temporary Google server issue."
                    )
            else:
                # For other errors, don't retry
                raise
    
    # If we get here, all retries failed
    raise last_error


def _get_client():
    """Lazily initialise the google.genai client."""
    global _client
    if _client is not None:
        return _client

    from app.config import settings
    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to backend/.env"
        )

    try:
        from google import genai
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
        logger.info("Gemini client initialised successfully")
        return _client
    except Exception as e:
        logger.error(f"Gemini client init failed: {e}")
        raise RuntimeError(f"Gemini init failed: {e}")


# ── Prompt templates ──────────────────────────────────────────────────────────

SYSTEM_INSTRUCTION = (
    "You are MediNova AI, a helpful healthcare assistant. "
    "You help patients understand their medical reports and answer general health questions. "
    "Always be empathetic, clear, and use simple non-technical language. "
    "NEVER provide a definitive diagnosis. "
    "ALWAYS end every response with this exact disclaimer on its own line:\n\n"
    "⚠️ This is AI-generated information and is not a substitute for professional medical advice. "
    "Please consult your doctor for medical decisions."
)

REPORT_ANALYSIS_PROMPT = """
You are analyzing a medical report that was extracted via OCR. The patient needs help understanding it.

EXTRACTED REPORT TEXT:
{ocr_text}

Please provide a structured analysis with these sections:
1. **Report Summary** – What type of report is this and what does it measure?
2. **Key Findings** – List the main results / values found.
3. **Abnormal Values** – Highlight any values outside normal ranges with ⚠️.
4. **Plain English Explanation** – What do these results mean in simple language?
5. **Recommended Actions** – What should the patient discuss with their doctor?

Do NOT diagnose any condition. Always recommend consulting a healthcare professional.

End your response with:
⚠️ This is AI-generated information and is not a substitute for professional medical advice. Please consult your doctor for medical decisions.
"""

DISCLAIMER = (
    "\n\n---\n⚠️ **This is AI-generated information and is not a substitute for "
    "professional medical advice. Please consult your doctor for medical decisions.**"
)


# ── AI Service ────────────────────────────────────────────────────────────────

class AIService:
    """Gemini AI service for medical report analysis and health chat."""

    # Model to use — gemini-3.6-flash is the current stable model
    MODEL = "gemini-3.6-flash"

    async def analyze_medical_report(self, ocr_text: str) -> Dict:
        """
        Analyze OCR-extracted medical report text.
        Returns a structured analysis with findings and plain-language explanation.
        """
        if not ocr_text or len(ocr_text.strip()) < 10:
            return {
                "success": False,
                "error": "Insufficient text. Please ensure the image/PDF is clear and readable."
            }

        try:
            client = _get_client()
            prompt = REPORT_ANALYSIS_PROMPT.format(ocr_text=ocr_text[:8000])

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
            
            response = await _retry_with_backoff(make_api_call, max_retries=3, initial_delay=2)

            text = response.text or ""
            if "⚠️ This is AI-generated" not in text:
                text += DISCLAIMER

            return {
                "success": True,
                "analysis": text,
                "analyzed_at": datetime.utcnow().isoformat(),
                "model": "gemini-2.0-flash-exp",
            }

        except RuntimeError as e:
            return {"success": False, "error": str(e), "fallback": True}
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return {"success": False, "error": f"Analysis failed: {str(e)}"}

    async def chat(self, message: str, history: List[Dict] = None) -> Dict:
        """
        Chat with the MediNova AI health assistant.

        Args:
            message: The user's latest message.
            history: List of previous turns [{"role": "user/assistant", "content": "..."}]

        Returns:
            Dict with 'success', 'response', 'timestamp', 'model'.
        """
        if not message or not message.strip():
            return {"success": False, "error": "Message cannot be empty"}

        try:
            from google.genai import types
            client = _get_client()

            # Build contents list from history + new message
            contents = []

            # Add conversation history
            for turn in (history or [])[-10:]:  # Keep last 10 for context
                role = turn.get("role")
                content = turn.get("content", "").strip()
                if content:
                    if role in ("user", "human"):
                        contents.append(types.Content(role="user", parts=[types.Part(text=content)]))
                    elif role in ("assistant", "model"):
                        contents.append(types.Content(role="model", parts=[types.Part(text=content)]))

            # Add the new user message
            contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

            # Use retry logic for API call
            async def make_api_call():
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(
                    None,
                    lambda: client.models.generate_content(
                        model="models/gemini-3.8-flash",
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            temperature=0.7,
                            max_output_tokens=1024,
                        )
                    )
                )
            
            response = await _retry_with_backoff(make_api_call, max_retries=3, initial_delay=2)

            text = response.text or ""
            if "⚠️ This is AI-generated" not in text:
                text += (
                    "\n\n⚠️ *This is AI-generated information and is not a substitute for "
                    "professional medical advice. Please consult your doctor for medical decisions.*"
                )

            return {
                "success": True,
                "response": text,
                "timestamp": datetime.utcnow().isoformat(),
                "model": self.MODEL,
            }

        except RuntimeError as e:
            # API key missing / not configured
            return {
                "success": False,
                "error": str(e),
                "fallback": True,
                "response": (
                    "I'm sorry, the AI assistant is not configured yet. "
                    "Please add your Gemini API key to `backend/.env`.\n\n"
                    "⚠️ This is AI-generated information and is not a substitute for professional medical advice."
                ),
            }
        except Exception as e:
            logger.error(f"AI chat error: {e}")
            return {"success": False, "error": f"Chat failed: {str(e)}"}

    async def is_available(self) -> bool:
        """Return True if the Gemini API key is configured."""
        from app.config import settings
        return bool(settings.GEMINI_API_KEY)


# Singleton
ai_service = AIService()
