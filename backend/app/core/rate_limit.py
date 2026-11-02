"""
Rate Limiting for MediNova AI
Implements production-safe rate limiting using slowapi with Redis backend
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import logging

from app.config import settings

logger = logging.getLogger(__name__)


def get_client_identifier(request: Request) -> str:
    """
    Get client identifier for rate limiting.
    
    Uses a combination of:
    1. Authenticated user ID if available
    2. Client IP address as fallback
    
    This prevents authenticated users from bypassing limits by changing IPs
    for user-specific limits, while using IP for auth endpoints.
    """
    # For authenticated endpoints, prefer user ID
    if hasattr(request.state, "user") and request.state.user:
        user_id = request.state.user.get("_id", "")
        if user_id:
            return f"user:{user_id}"
    
    # For unauthenticated endpoints (login, register), use IP
    # Safely extract client IP, handling proxies
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # Take first IP in chain (actual client), but validate it
        ip = forwarded.split(",")[0].strip()
        # Basic validation to prevent header injection
        if ip and all(c.isdigit() or c == '.' or c == ':' for c in ip):
            return f"ip:{ip}"
    
    # Fallback to direct connection IP
    if request.client:
        return f"ip:{request.client.host}"
    
    # Ultimate fallback
    return "ip:unknown"


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Custom handler for rate limit exceeded errors.
    Returns 429 with appropriate headers and message.
    """
    # Extract retry-after if available
    retry_after = None
    if hasattr(exc, "retry_after"):
        retry_after = exc.retry_after
    
    response_data = {
        "error": "rate_limit_exceeded",
        "message": "Too many requests. Please try again later.",
        "detail": "Rate limit exceeded. Please wait before making more requests."
    }
    
    headers = {}
    if retry_after:
        headers["Retry-After"] = str(int(retry_after))
    
    logger.warning(
        f"Rate limit exceeded for {get_client_identifier(request)} "
        f"on {request.url.path}"
    )
    
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content=response_data,
        headers=headers
    )


def _validate_redis_in_production():
    """
    Validate Redis configuration in production.
    Warns if memory-based rate limiting is used in production (allows free tier deployment).
    """
    if settings.is_production:
        redis_url = settings.REDIS_URL
        
        # Warn if Redis URL is not properly configured (but allow deployment for free tier)
        if not redis_url or redis_url == "memory://":
            logger.warning(
                "WARNING: Using memory-based rate limiting in production. "
                "This is suitable for single-instance deployments (like Render free tier) "
                "but not recommended for multi-worker production environments. "
                "Consider using Redis for better rate limiting: Set REDIS_URL environment variable."
            )
        
        if not redis_url.startswith("redis://") and not redis_url.startswith("rediss://"):
            raise RuntimeError(
                f"CRITICAL: Invalid REDIS_URL format: {redis_url}. "
                "Must start with 'redis://' or 'rediss://' for secure connection."
            )
        
        logger.info(f"Rate limiting configured with Redis (production mode)")
    else:
        logger.info(f"Rate limiting configured with storage: {settings.REDIS_URL}")


# Initialize limiter with Redis backend
if settings.RATE_LIMIT_ENABLED:
    # Validate Redis configuration in production
    _validate_redis_in_production()
    
    # Create limiter with appropriate storage backend
    limiter = Limiter(
        key_func=get_client_identifier,
        default_limits=[settings.RATE_LIMIT_DEFAULT],
        enabled=True,
        storage_uri=settings.REDIS_URL,
        strategy="fixed-window",  # Simple and predictable
        headers_enabled=True  # Include X-RateLimit-* headers in responses
    )
    
    logger.info(f"Rate limiting enabled with storage: {settings.REDIS_URL.split('@')[-1]}")  # Don't log credentials
else:
    # Disabled limiter for development flexibility
    limiter = Limiter(
        key_func=get_client_identifier,
        default_limits=[],
        enabled=False
    )
    logger.info("Rate limiting disabled")


# Specific limit decorators for common use cases
def limit_login():
    """Rate limit for login endpoint (IP-based)"""
    return limiter.limit(settings.RATE_LIMIT_LOGIN, per_method=True)


def limit_register():
    """Rate limit for registration endpoint (IP-based)"""
    return limiter.limit(settings.RATE_LIMIT_REGISTER, per_method=True)


def limit_password():
    """Rate limit for password change endpoint (IP-based)"""
    return limiter.limit(settings.RATE_LIMIT_PASSWORD, per_method=True)


def limit_ai_chat():
    """Rate limit for AI chat endpoint (user-based)"""
    return limiter.limit(settings.RATE_LIMIT_AI_CHAT, per_method=True)


def limit_ai_analyze():
    """Rate limit for AI analysis endpoint (user-based)"""
    return limiter.limit(settings.RATE_LIMIT_AI_ANALYZE, per_method=True)


def limit_ocr():
    """Rate limit for OCR endpoint (user-based)"""
    return limiter.limit(settings.RATE_LIMIT_OCR, per_method=True)


def limit_email_verification():
    """Rate limit for email verification resend (IP-based)"""
    return limiter.limit("3/hour", per_method=True)


def limit_password_reset():
    """Rate limit for password reset requests (IP-based)"""
    return limiter.limit("3/hour", per_method=True)
