from typing import Optional
from pydantic import Field, EmailStr
from fluvius.data import DataModel
import uuid

class SignUpData(DataModel):
    """Data model for user sign-up information."""
    
    username: str = Field(..., description="The username of the new user.", min_length=3, max_length=255)
    email: EmailStr = Field(..., description="The email address of the new user.")
    password: str = Field(..., description="The password for the new user.", min_length=8)
    first_name: Optional[str] = Field(None, description="First name of the user.", max_length=255)
    last_name: Optional[str] = Field(None, description="Last name of the user.", max_length=255)
    phone: Optional[str] = Field(None, description="Phone number of the user.", max_length=50)


class SignInData(DataModel):
    """Data model for user sign-in (login) information."""
    
    username: str = Field(..., description="The username or email of the user.", min_length=3, max_length=255)
    password: str = Field(..., description="The password for the user.", min_length=1)


class LogOutData(DataModel):
    """Data model for user log-out information."""
    
    user_id: uuid.UUID = Field(..., description="The user ID to logout.")
    session_id: Optional[uuid.UUID] = Field(None, description="The specific session ID to invalidate (optional).")


class AuthTokenResponse(DataModel):
    """Response data model for authentication tokens."""
    
    access_token: str = Field(..., description="JWT access token.")
    token_type: str = Field(default="Bearer", description="Token type.")
    expires_in: int = Field(..., description="Token expiration time in seconds.")
    user_id: uuid.UUID = Field(..., description="The authenticated user ID.")
    username: str = Field(..., description="The authenticated username.")