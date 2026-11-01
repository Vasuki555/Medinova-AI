"""
Input Validation Utilities
Comprehensive validation functions for common input patterns
"""

import re
from typing import Optional
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status


def validate_object_id(id_string: str, field_name: str = "ID") -> ObjectId:
    """
    Validate and convert string to MongoDB ObjectId
    
    Args:
        id_string: String representation of ObjectId
        field_name: Name of field for error messages
        
    Returns:
        Valid ObjectId instance
        
    Raises:
        HTTPException 400: If ID format is invalid
    """
    if not id_string:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} is required"
        )
    
    try:
        return ObjectId(id_string)
    except (InvalidId, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {field_name} format. Must be a valid MongoDB ObjectId (24 hex characters)"
        )


def validate_date_string(date_string: str, field_name: str = "Date") -> datetime:
    """
    Validate and parse ISO 8601 date string
    
    Args:
        date_string: ISO 8601 formatted date string
        field_name: Name of field for error messages
        
    Returns:
        Parsed datetime object
        
    Raises:
        HTTPException 400: If date format is invalid
    """
    if not date_string:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} is required"
        )
    
    try:
        # Try parsing ISO format
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {field_name} format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)"
        )


def validate_email(email: str) -> str:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        Lowercase email string
        
    Raises:
        HTTPException 400: If email format is invalid
    """
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )
    
    # Basic email pattern - Pydantic EmailStr is better but this is for manual validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    return email.lower()


def validate_phone(phone: str) -> str:
    """
    Validate phone number in E.164 format
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Validated phone string
        
    Raises:
        HTTPException 400: If phone format is invalid
    """
    if not phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number is required"
        )
    
    # E.164 format: +[country code][number]
    pattern = r'^\+?[1-9]\d{1,14}$'
    if not re.match(pattern, phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone format. Use E.164 format (e.g., +14155552671)"
        )
    
    return phone


def validate_file_mime_type(filename: str, content_type: str, allowed_types: list) -> None:
    """
    Validate file MIME type against allowed types
    
    Args:
        filename: Name of the uploaded file
        content_type: MIME type from request
        allowed_types: List of allowed MIME types
        
    Raises:
        HTTPException 400: If file type is not allowed
    """
    if not content_type or content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )
    
    # Additional validation: check file extension matches MIME type
    extension_map = {
        'image/jpeg': ['.jpg', '.jpeg'],
        'image/png': ['.png'],
        'image/webp': ['.webp'],
        'image/bmp': ['.bmp'],
        'application/pdf': ['.pdf']
    }
    
    if content_type in extension_map:
        valid_extensions = extension_map[content_type]
        if not any(filename.lower().endswith(ext) for ext in valid_extensions):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File extension does not match MIME type. Expected: {', '.join(valid_extensions)}"
            )


def validate_pagination(page: int = 1, page_size: int = 10, max_page_size: int = 100) -> tuple:
    """
    Validate pagination parameters
    
    Args:
        page: Page number (1-indexed)
        page_size: Items per page
        max_page_size: Maximum allowed page size
        
    Returns:
        Tuple of (validated_page, validated_page_size, skip)
        
    Raises:
        HTTPException 400: If pagination parameters are invalid
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page number must be >= 1"
        )
    
    if page_size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be >= 1"
        )
    
    if page_size > max_page_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Page size must be <= {max_page_size}"
        )
    
    skip = (page - 1) * page_size
    return page, page_size, skip


def validate_date_range(start_date: Optional[str], end_date: Optional[str]) -> tuple:
    """
    Validate date range
    
    Args:
        start_date: Start date string (ISO 8601)
        end_date: End date string (ISO 8601)
        
    Returns:
        Tuple of (start_datetime, end_datetime)
        
    Raises:
        HTTPException 400: If date range is invalid
    """
    start_dt = None
    end_dt = None
    
    if start_date:
        start_dt = validate_date_string(start_date, "Start date")
    
    if end_date:
        end_dt = validate_date_string(end_date, "End date")
    
    if start_dt and end_dt and start_dt > end_dt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before or equal to end date"
        )
    
    return start_dt, end_dt


def sanitize_string(text: str, max_length: int = 1000) -> str:
    """
    Sanitize user input string
    
    Args:
        text: Input string to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
        
    Raises:
        HTTPException 400: If string exceeds max length
    """
    if not text:
        return ""
    
    # Remove null bytes and control characters
    sanitized = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    if len(sanitized) > max_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Text exceeds maximum length of {max_length} characters"
        )
    
    return sanitized


def validate_enum_value(value: str, allowed_values: list, field_name: str = "Value") -> str:
    """
    Validate value against allowed enum values
    
    Args:
        value: Value to validate
        allowed_values: List of allowed values
        field_name: Name of field for error messages
        
    Returns:
        Validated value (lowercase)
        
    Raises:
        HTTPException 400: If value is not in allowed list
    """
    if not value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} is required"
        )
    
    value_lower = value.lower()
    allowed_lower = [v.lower() for v in allowed_values]
    
    if value_lower not in allowed_lower:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {field_name}. Allowed values: {', '.join(allowed_values)}"
        )
    
    return value_lower


def validate_numeric_range(
    value: float,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    field_name: str = "Value"
) -> float:
    """
    Validate numeric value is within range
    
    Args:
        value: Numeric value to validate
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)
        field_name: Name of field for error messages
        
    Returns:
        Validated numeric value
        
    Raises:
        HTTPException 400: If value is out of range
    """
    if min_value is not None and value < min_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} must be >= {min_value}"
        )
    
    if max_value is not None and value > max_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} must be <= {max_value}"
        )
    
    return value
