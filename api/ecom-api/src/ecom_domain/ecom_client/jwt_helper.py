"""JWT Helper utilities for authentication token management."""

import jwt
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from fluvius.error import BadRequestError

from . import config

# JWT Configuration
JWT_SECRET_KEY = config.JWT_SECRET_KEY if hasattr(config, 'JWT_SECRET_KEY') else "your-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = config.JWT_EXPIRATION_HOURS if hasattr(config, 'JWT_EXPIRATION_HOURS') else 24


class JWTHelper:
    """Helper class for JWT token management."""

    @staticmethod
    def create_token(
        user_id: uuid.UUID,
        username: str,
        expires_in_hours: int = JWT_EXPIRATION_HOURS,
        additional_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a JWT access token for a user.
        
        Args:
            user_id: User ID to encode in token
            username: Username to encode in token
            expires_in_hours: Token expiration time in hours (default: 24)
            additional_claims: Additional claims to include in token payload (optional)
            
        Returns:
            JWT token string
            
        Example:
            >>> token = JWTHelper.create_token(user_id=uuid.uuid4(), username="john_doe")
            >>> print(token)
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        """
        now = datetime.now(timezone.utc)
        expire_time = now + timedelta(hours=expires_in_hours)
        
        payload = {
            "user_id": str(user_id),
            "username": username,
            "exp": expire_time,
            "iat": now,
            "type": "access"
        }
        
        # Add additional claims if provided
        if additional_claims:
            payload.update(additional_claims)
        
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token

    @staticmethod
    def create_refresh_token(user_id: uuid.UUID, expires_in_days: int = 7) -> str:
        """
        Create a JWT refresh token for a user.
        
        Args:
            user_id: User ID to encode in token
            expires_in_days: Token expiration time in days (default: 7)
            
        Returns:
            JWT refresh token string
        """
        now = datetime.now(timezone.utc)
        expire_time = now + timedelta(days=expires_in_days)
        
        payload = {
            "user_id": str(user_id),
            "exp": expire_time,
            "iat": now,
            "type": "refresh"
        }
        
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token

    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload as dictionary
            
        Raises:
            BadRequestError: If token is invalid, expired, or malformed
            
        Example:
            >>> payload = JWTHelper.verify_token(token)
            >>> user_id = payload.get("user_id")
        """
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise BadRequestError(
                "AUTH.TOKEN_EXPIRED",
                "Token has expired. Please sign in again."
            )
        except jwt.InvalidTokenError as e:
            raise BadRequestError(
                "AUTH.INVALID_TOKEN",
                f"Invalid token: {str(e)}"
            )
        except Exception as e:
            raise BadRequestError(
                "AUTH.TOKEN_ERROR",
                f"Token validation error: {str(e)}"
            )

    @staticmethod
    def extract_user_id(token: str) -> uuid.UUID:
        """
        Extract user ID from a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            User ID as UUID
            
        Raises:
            BadRequestError: If token is invalid or doesn't contain user_id
        """
        payload = JWTHelper.verify_token(token)
        user_id_str = payload.get("user_id")
        
        if not user_id_str:
            raise BadRequestError(
                "AUTH.NO_USER_ID",
                "Token does not contain user_id claim."
            )
        
        try:
            return uuid.UUID(user_id_str)
        except ValueError:
            raise BadRequestError(
                "AUTH.INVALID_USER_ID",
                "Invalid user_id format in token."
            )

    @staticmethod
    def extract_username(token: str) -> str:
        """
        Extract username from a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Username string
            
        Raises:
            BadRequestError: If token is invalid or doesn't contain username
        """
        payload = JWTHelper.verify_token(token)
        username = payload.get("username")
        
        if not username:
            raise BadRequestError(
                "AUTH.NO_USERNAME",
                "Token does not contain username claim."
            )
        
        return username

    @staticmethod
    def is_token_expired(token: str) -> bool:
        """
        Check if a JWT token is expired.
        
        Args:
            token: JWT token string
            
        Returns:
            True if token is expired, False otherwise
        """
        try:
            JWTHelper.verify_token(token)
            return False
        except BadRequestError as e:
            if "expired" in str(e).lower():
                return True
            raise

    @staticmethod
    def get_time_remaining(token: str) -> Optional[timedelta]:
        """
        Get the remaining time until token expiration.
        
        Args:
            token: JWT token string
            
        Returns:
            timedelta object with remaining time, or None if token is invalid
        """
        try:
            payload = JWTHelper.verify_token(token)
            exp_timestamp = payload.get("exp")
            
            if not exp_timestamp:
                return None
            
            exp_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            remaining = exp_time - datetime.now(timezone.utc)
            return remaining if remaining.total_seconds() > 0 else None
        except BadRequestError:
            return None


class TokenPayload:
    """Data class for parsed JWT token payload."""
    
    def __init__(self, payload: Dict[str, Any]):
        """Initialize with decoded JWT payload."""
        self.user_id = uuid.UUID(payload.get("user_id")) if payload.get("user_id") else None
        self.username = payload.get("username")
        self.exp = payload.get("exp")
        self.iat = payload.get("iat")
        self.token_type = payload.get("type", "access")
        self.additional_claims = {k: v for k, v in payload.items() 
                                 if k not in ["user_id", "username", "exp", "iat", "type"]}
    
    def is_expired(self) -> bool:
        """Check if token is expired."""
        if not self.exp:
            return False
        return datetime.fromtimestamp(self.exp, tz=timezone.utc) <= datetime.now(timezone.utc)
    
    def is_access_token(self) -> bool:
        """Check if this is an access token."""
        return self.token_type == "access"
    
    def is_refresh_token(self) -> bool:
        """Check if this is a refresh token."""
        return self.token_type == "refresh"
