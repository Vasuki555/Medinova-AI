"""
Session Management Service
Handles user session tracking and refresh token revocation
"""

import logging
from typing import Optional
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config import settings

logger = logging.getLogger(__name__)


class SessionService:
    """Session service for managing user sessions and token revocation"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.sessions_collection = db.user_sessions
        self.revoked_tokens_collection = db.revoked_tokens
    
    async def create_session(self, user_id: str, refresh_token_jti: str) -> None:
        """
        Create a new user session
        
        Args:
            user_id: User ID
            refresh_token_jti: JWT ID of the refresh token
        """
        session = {
            "user_id": user_id,
            "refresh_token_jti": refresh_token_jti,
            "created_at": datetime.utcnow(),
            "last_used_at": datetime.utcnow(),
            "is_active": True,
            "revoked_at": None
        }
        
        await self.sessions_collection.insert_one(session)
    
    async def revoke_token(self, token_jti: str, token_type: str = "refresh") -> bool:
        """
        Revoke a token by adding it to revoked tokens list
        
        Args:
            token_jti: JWT ID to revoke
            token_type: Type of token (refresh or access)
        
        Returns:
            True if successfully revoked
        """
        try:
            # Add to revoked tokens
            revoked_token = {
                "jti": token_jti,
                "token_type": token_type,
                "revoked_at": datetime.utcnow(),
                # TTL: tokens expire anyway, so we can clean up after expiration
                "expires_at": datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
            }
            
            await self.revoked_tokens_collection.insert_one(revoked_token)
            
            # Mark session as inactive
            await self.sessions_collection.update_one(
                {"refresh_token_jti": token_jti},
                {
                    "$set": {
                        "is_active": False,
                        "revoked_at": datetime.utcnow()
                    }
                }
            )
            
            logger.info(f"Token revoked: {token_jti[:8]}...")
            return True
            
        except Exception as e:
            logger.error(f"Failed to revoke token: {e}")
            return False
    
    async def is_token_revoked(self, token_jti: str) -> bool:
        """
        Check if a token has been revoked
        
        Args:
            token_jti: JWT ID to check
        
        Returns:
            True if token is revoked
        """
        revoked = await self.revoked_tokens_collection.find_one({"jti": token_jti})
        return revoked is not None
    
    async def revoke_all_user_sessions(self, user_id: str) -> int:
        """
        Revoke all active sessions for a user
        
        Args:
            user_id: User ID
        
        Returns:
            Number of sessions revoked
        """
        # Find all active sessions
        active_sessions = await self.sessions_collection.find({
            "user_id": user_id,
            "is_active": True
        }).to_list(length=100)
        
        count = 0
        for session in active_sessions:
            jti = session.get("refresh_token_jti")
            if jti:
                await self.revoke_token(jti)
                count += 1
        
        logger.info(f"Revoked {count} sessions for user {user_id}")
        return count
    
    async def cleanup_expired_tokens(self) -> int:
        """
        Clean up expired revoked tokens
        
        Returns:
            Number of expired tokens cleaned up
        """
        result = await self.revoked_tokens_collection.delete_many({
            "expires_at": {"$lt": datetime.utcnow()}
        })
        
        cleaned = result.deleted_count
        if cleaned > 0:
            logger.info(f"Cleaned up {cleaned} expired revoked tokens")
        
        return cleaned
    
    async def get_user_sessions(self, user_id: str) -> list:
        """
        Get all sessions for a user
        
        Args:
            user_id: User ID
        
        Returns:
            List of user sessions
        """
        sessions = await self.sessions_collection.find({
            "user_id": user_id
        }).sort("created_at", -1).to_list(length=50)
        
        for session in sessions:
            session["_id"] = str(session["_id"])
        
        return sessions
