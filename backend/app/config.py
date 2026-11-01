"""
Configuration Management
Loads environment variables and provides application configuration
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application Configuration
    APP_NAME: str = "MediNova AI"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Multi-Agent Healthcare Intelligence Platform"
    ENVIRONMENT: str = "development"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True
    
    # MongoDB Configuration
    MONGODB_URL: str
    MONGODB_DB_NAME: str = "medinova_ai"
    MONGODB_MIN_POOL_SIZE: int = 10
    MONGODB_MAX_POOL_SIZE: int = 50
    
    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str = ""  # Separate secret for refresh tokens (optional but recommended)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = "*"
    CORS_ALLOW_HEADERS: str = "*"
    
    # Frontend URL (for QR codes and redirects)
    FRONTEND_URL: str = "http://localhost:5173"
    
    # AI Configuration — Google Gemini
    GEMINI_API_KEY: str = ""
    # Legacy OpenAI key (kept for backward compatibility)
    OPENAI_API_KEY: str = ""
    
    # Google Maps API Configuration
    GOOGLE_MAPS_API_KEY: str = ""
    
    # File Upload Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE_MB: int = 50  # Increased to 50MB for medical reports
    ALLOWED_IMAGE_TYPES: str = "image/jpeg,image/png,image/webp,image/bmp"
    ALLOWED_DOC_TYPES: str = "application/pdf"
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Rate Limiting Configuration
    RATE_LIMIT_ENABLED: bool = True
    REDIS_URL: str = "memory://"  # Redis URL for rate limiting (use "redis://localhost:6379" for production)
    
    # Email Configuration (SMTP)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@medinova.ai"
    SMTP_FROM_NAME: str = "MediNova AI"
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:5173/auth/google/callback"
    
    # Authentication endpoints (per IP)
    # Production values: strict limits to prevent brute force attacks
    # For development testing, you can increase these in .env file
    RATE_LIMIT_LOGIN: str = "5/15minutes"  # 5 attempts per 15 minutes
    RATE_LIMIT_REGISTER: str = "5/hour"  # 5 registrations per hour
    RATE_LIMIT_PASSWORD: str = "5/15minutes"  # 5 password changes per 15 minutes
    
    # AI/ML endpoints (per user)
    # Moderate limits to prevent API abuse while allowing normal usage
    RATE_LIMIT_AI_CHAT: str = "30/minute"  # 30 AI chat requests per minute per user
    RATE_LIMIT_AI_ANALYZE: str = "10/minute"  # 10 analysis requests per minute per user
    
    # OCR endpoints (per user)
    # OCR is resource-intensive, keep limits conservative
    RATE_LIMIT_OCR: str = "10/minute"  # 10 OCR extractions per minute per user
    
    # Global fallback
    RATE_LIMIT_DEFAULT: str = "100/minute"  # Default for other endpoints
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """
        Parse CORS origins string into list.
        In production, filters out localhost origins for security.
        If no production origins are configured, raises an error to prevent misconfiguration.
        """
        origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        
        # In production, exclude localhost origins and validate configuration
        if self.is_production:
            production_origins = [o for o in origins if "localhost" not in o and "127.0.0.1" not in o]
            
            if not production_origins:
                # FAIL FAST: Production must have valid origins configured
                raise ValueError(
                    "CORS_ORIGINS not configured for production environment. "
                    "You must set production domain(s) in CORS_ORIGINS environment variable. "
                    "Example: CORS_ORIGINS=https://app.medinova.ai,https://www.medinova.ai"
                )
            
            return production_origins
        
        # Development: return all origins including localhost
        return origins
    
    @property
    def allowed_image_types_list(self) -> List[str]:
        return [t.strip() for t in self.ALLOWED_IMAGE_TYPES.split(",")]
    
    @property
    def allowed_doc_types_list(self) -> List[str]:
        return [t.strip() for t in self.ALLOWED_DOC_TYPES.split(",")]
    
    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    
    @property
    def upload_dir_path(self) -> str:
        """Absolute path to uploads directory"""
        return os.path.abspath(self.UPLOAD_DIR)
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT.lower() == "development"


# Global settings instance
settings = Settings()
