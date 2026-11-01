"""
AI Router
FastAPI endpoints for AI-powered medical report analysis and health chat assistant
"""

import logging
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel
from bson import ObjectId

from app.database import get_database
from app.core.dependencies import get_current_user
from app.services.ai_service import ai_service
from app.core.rate_limit import limit_ai_chat, limit_ai_analyze

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["AI Assistant"])


# ── Pydantic Schemas ──────────────────────────────────────────────────────────

class ReportAnalysisRequest(BaseModel):
    ocr_text: str
    report_type: Optional[str] = None  # "blood_test", "xray", "mri", etc.
    health_record_id: Optional[str] = None  # Link analysis to a health record


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []
    context: Optional[str] = None  # e.g. "patient has diabetes"


class AnalysisResponse(BaseModel):
    success: bool
    analysis: Optional[str] = None
    analyzed_at: Optional[str] = None
    model: Optional[str] = None
    error: Optional[str] = None


class ChatResponse(BaseModel):
    success: bool
    response: Optional[str] = None
    timestamp: Optional[str] = None
    error: Optional[str] = None


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/status")
async def get_ai_status(current_user: dict = Depends(get_current_user)):
    """Check if AI assistant is configured and available."""
    available = await ai_service.is_available()
    return {
        "available": available,
        "model": "gemini-1.5-flash" if available else None,
        "message": (
            "AI assistant is ready" if available
            else "AI assistant is not configured. Add GEMINI_API_KEY to backend/.env"
        )
    }


@router.post(
    "/analyze-report",
    summary="Analyze Medical Report",
    description="""
    Analyze OCR-extracted medical report text using Gemini AI.
    
    **Rate Limit:** 10 analysis requests per minute per user
    
    - Identifies report type and key values
    - Highlights abnormal results with ⚠️
    - Explains findings in plain language
    - Provides suggested discussion points for doctor visits
    
    Returns AI analysis with mandatory disclaimer.
    """,
    responses={
        200: {
            "description": "Analysis completed"
        },
        400: {
            "description": "Invalid or insufficient OCR text"
        },
        429: {
            "description": "Too many analysis requests. Rate limit exceeded."
        }
    }
)
@limit_ai_analyze()
async def analyze_report(
    request: Request,
    response: Response,
    analysis_request: ReportAnalysisRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Analyze OCR-extracted medical report text using Gemini AI.
    
    - Identifies report type and key values
    - Highlights abnormal results with ⚠️
    - Explains findings in plain language
    - Provides suggested discussion points for doctor visits
    - Rate limited to 10 requests per minute per user
    
    Returns AI analysis with mandatory disclaimer.
    """
    if not analysis_request.ocr_text or len(analysis_request.ocr_text.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ocr_text is required and must have at least 10 characters"
        )

    result = await ai_service.analyze_medical_report(analysis_request.ocr_text)

    # Store AI analysis in database if health_record_id provided
    if result.get("success") and analysis_request.health_record_id:
        try:
            await db.ai_reports.insert_one({
                "user_id": current_user["_id"],
                "health_record_id": analysis_request.health_record_id,
                "report_type": analysis_request.report_type,
                "ocr_text": analysis_request.ocr_text[:5000],  # Store first 5000 chars
                "analysis": result.get("analysis"),
                "model": result.get("model"),
                "analyzed_at": datetime.utcnow(),
                "created_at": datetime.utcnow()
            })
        except Exception as e:
            logger.warning(f"Could not save AI report: {e}")

    if not result.get("success"):
        # Return 200 with error info — frontend handles gracefully
        return {
            "success": False,
            "error": result.get("error", "Analysis failed"),
            "fallback": result.get("fallback", False)
        }

    return result


@router.post(
    "/chat",
    summary="Chat with AI Assistant",
    description="""
    Chat with MediNova AI health assistant.
    
    **Rate Limit:** 30 chat messages per minute per user
    
    - Answers health questions in plain language
    - Provides report-related Q&A
    - Maintains conversation context via history
    - Never diagnoses — always recommends consulting a doctor
    
    Always includes: "⚠️ This is AI-generated information..."
    """,
    responses={
        200: {
            "description": "Chat response generated"
        },
        400: {
            "description": "Empty message"
        },
        429: {
            "description": "Too many chat requests. Rate limit exceeded."
        }
    }
)
@limit_ai_chat()
async def chat_with_assistant(
    request: Request,
    response: Response,
    chat_request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Chat with MediNova AI health assistant.
    
    - Answers health questions in plain language
    - Provides report-related Q&A
    - Maintains conversation context via history
    - Never diagnoses — always recommends consulting a doctor
    - Rate limited to 30 messages per minute per user
    
    Always includes: "⚠️ This is AI-generated information..."
    """
    if not chat_request.message or not chat_request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )

    # Convert ChatMessage objects to dicts for service
    history = [
        {"role": msg.role, "content": msg.content}
        for msg in (chat_request.history or [])
    ]

    result = await ai_service.chat(chat_request.message, history)

    # Save conversation turn to DB
    try:
        await db.ai_conversations.insert_one({
            "user_id": current_user["_id"],
            "user_message": chat_request.message,
            "assistant_response": result.get("response"),
            "success": result.get("success"),
            "timestamp": datetime.utcnow(),
            "model": result.get("model")
        })
    except Exception as e:
        logger.warning(f"Could not save conversation: {e}")

    return result


@router.get("/chat/history")
async def get_chat_history(
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Retrieve recent AI conversation history for the current user.
    Returns the last N conversation turns.
    """
    cursor = db.ai_conversations.find(
        {"user_id": current_user["_id"]},
        {"_id": 0}
    ).sort("timestamp", -1).limit(limit)

    conversations = await cursor.to_list(limit)

    # Reverse to chronological order
    conversations.reverse()

    return {
        "history": conversations,
        "total": len(conversations)
    }


@router.get("/reports")
async def get_ai_reports(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Retrieve all AI-analyzed medical reports for the current user."""
    cursor = db.ai_reports.find(
        {"user_id": current_user["_id"]},
        {"ocr_text": 0}  # Exclude raw OCR text from listing
    ).sort("analyzed_at", -1).limit(50)

    reports = await cursor.to_list(50)
    for r in reports:
        r["id"] = str(r.pop("_id", ""))

    return reports
