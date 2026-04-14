# Authentication Implementation Guide

## Overview

This document describes the complete authentication system implemented for the eCommerce GraphRAG project. The system supports user sign-up, sign-in (login), and logout with JWT token-based authentication.

## Components

### 1. Data Models (`datadef.py`)

#### SignUpData
Request model for user registration.

```python
class SignUpData(DataModel):
    username: str  # 3-255 characters, unique
    email: EmailStr  # Valid email, unique
    password: str  # Minimum 8 characters
    first_name: Optional[str]  # User's first name
    last_name: Optional[str]  # User's last name
    phone: Optional[str]  # Phone number
```

#### SignInData
Request model for user login.

```python
class SignInData(DataModel):
    username: str  # Username or email address
    password: str  # User's password
```

#### LogOutData
Request model for user logout.

```python
class LogOutData(DataModel):
    user_id: uuid.UUID  # User's ID
    session_id: Optional[uuid.UUID]  # Specific session to logout (optional - logout all if not provided)
```

#### AuthTokenResponse
Response model for authentication tokens.

```python
class AuthTokenResponse(DataModel):
    access_token: str  # JWT access token
    token_type: str = "Bearer"  # Token type (always "Bearer")
    expires_in: int  # Token expiration time in seconds
    user_id: uuid.UUID  # Authenticated user's ID
    username: str  # Authenticated user's username
```

### 2. Commands (`command.py`)

#### SignUpCommand
Handles user registration and creates a new user account.

**Request key:** `sign-up`

**Payload:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User registered successfully.",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "john_doe",
    "email": "john@example.com",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 86400,
    "session_id": "550e8400-e29b-41d4-a716-446655440001"
  }
}
```

**Features:**
- Validates username and email uniqueness
- Hashes password using bcrypt (rounds=12)
- Creates user record with ACTIVE status
- Creates related user identity and profile
- Generates JWT access token valid for 24 hours
- Creates initial user session

#### SignInCommand
Handles user login and generates authentication token.

**Request key:** `sign-in`

**Payload:**
```json
{
  "username": "john_doe",
  "password": "SecurePassword123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Sign in successful.",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "john_doe",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 86400,
    "session_id": "550e8400-e29b-41d4-a716-446655440002"
  }
}
```

**Features:**
- Finds user by username or email
- Verifies password using bcrypt
- Validates user account status
- Generates new JWT access token
- Creates new session record
- Updates last login timestamp

#### LogOutCommand
Handles user logout and invalidates sessions.

**Request key:** `log-out`

**Payload (logout from all sessions):**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Payload (logout from specific session):**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "550e8400-e29b-41d4-a716-446655440002"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Sign out successful.",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "logged_out_at": "2024-01-15T10:30:00+00:00"
  }
}
```

**Features:**
- Validates user existence
- Invalidates specific session or all sessions
- Removes session records from database

### 3. Aggregate Methods (`aggregate.py`)

The `EcomClientAggregate` class provides the core authentication logic:

#### Password Management

```python
# Hash a plain text password
hashed = aggregate.hash_password("MyPassword123")

# Verify a password against its hash
is_valid = aggregate.verify_password("MyPassword123", hashed)
```

#### JWT Token Management

```python
# Generate a new JWT token
token = aggregate.generate_jwt_token(
    user_id=user_id,
    username="john_doe",
    expires_in_hours=24
)

# Verify and decode a JWT token
payload = aggregate.verify_jwt_token(token)
# Returns: {"user_id": "...", "username": "...", "exp": ..., "iat": ..., "type": "access"}
```

#### User Management

```python
# Check if user exists
exists = await aggregate.check_user_exists(stm, "john_doe", "john@example.com")

# Create new user with profile and identity
user_data = await aggregate.create_user(
    stm=stm,
    user_id=new_user_id,
    username="john_doe",
    email="john@example.com",
    password="SecurePassword123",
    first_name="John",
    last_name="Doe",
    phone="+1234567890"
)

# Get user by ID
user = await aggregate.get_user(stm, user_id)

# Get user identity by username or email
identity = await aggregate.get_user_identity(stm, "john_doe")
```

#### Session Management

```python
# Create a new session
session_data = await aggregate.create_session(
    stm=stm,
    user_id=user_id,
    session_id=session_id,
    source=UserSourceEnum.WEB,
    email="john@example.com"
)

# Update last login timestamp
await aggregate.update_last_login(stm, user_id)

# Invalidate a specific session
await aggregate.invalidate_session(stm, session_id)

# Invalidate all sessions for a user
await aggregate.invalidate_all_sessions(stm, user_id)
```

### 4. JWT Helper Utilities (`jwt_helper.py`)

The `JWTHelper` class provides convenient JWT token operations:

```python
from ecom_domain.ecom_client import JWTHelper
import uuid

# Create an access token
token = JWTHelper.create_token(
    user_id=uuid.uuid4(),
    username="john_doe",
    expires_in_hours=24,
    additional_claims={"role": "user"}
)

# Create a refresh token
refresh_token = JWTHelper.create_refresh_token(
    user_id=uuid.uuid4(),
    expires_in_days=7
)

# Verify and decode a token
payload = JWTHelper.verify_token(token)

# Extract user ID from token
user_id = JWTHelper.extract_user_id(token)

# Extract username from token
username = JWTHelper.extract_username(token)

# Check if token is expired
is_expired = JWTHelper.is_token_expired(token)

# Get time remaining until token expiration
remaining = JWTHelper.get_time_remaining(token)
if remaining:
    print(f"Token valid for {remaining.total_seconds()} seconds")
```

#### TokenPayload Class
Parse and inspect JWT token claims:

```python
payload = JWTHelper.verify_token(token)
token_payload = TokenPayload(payload)

print(f"User ID: {token_payload.user_id}")
print(f"Username: {token_payload.username}")
print(f"Is Access Token: {token_payload.is_access_token()}")
print(f"Is Expired: {token_payload.is_expired()}")
```

## Database Schema

### User Table (`ecom_client.user`)
- `_id` (UUID, Primary Key)
- `username` (String, Unique)
- `active` (Boolean, Default: True)
- `status` (Enum: NEW, ACTIVE, INACTIVE, PENDING, EXPIRED, DEACTIVATED)
- `is_super_admin` (Boolean, Default: False)
- `last_verified_request` (DateTime, nullable)
- `_created` (DateTime, Default: now())

### UserIdentity Table (`ecom_client.user_identity`)
- `_id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key to user)
- `provider` (String, Default: "local")
- `provider_user_id` (String)
- `active` (Boolean, Default: True)
- `telecom__email` (String, Unique)
- `telecom__phone` (String, nullable)
- `password_hash` (String, nullable)

### UserSession Table (`ecom_client.user_session`)
- `_id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key to user)
- `user_identity_id` (UUID, Foreign Key to user_identity, nullable)
- `source` (Enum: WEB, MOBILE, KEYCLOAK, MOBILE_KC, DASHBOARD, WEBSITE)
- `telecom__email` (String, nullable)
- `_created` (DateTime, Default: now())

### Profile Table (`ecom_client.profile`)
- `_id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key to user)
- `username` (String, nullable)
- `telecom__email` (String, nullable)
- `telecom__phone` (String, nullable)
- `name__given` (String, nullable)
- `name__family` (String, nullable)
- `verified_email` (String, nullable)
- `last_login` (DateTime, nullable)
- `status` (Enum: NEW, ACTIVE, INACTIVE, PENDING, EXPIRED, DEACTIVATED)
- `current_profile` (Boolean, Default: False)
- `_created` (DateTime, Default: now())

## Error Handling

The system includes comprehensive error handling with error codes:

| Error Code | Description | HTTP Status |
|-----------|-------------|------------|
| `USER.001` | Username or email already registered | 400 |
| `USER.002` | Failed to register user | 500 |
| `USER.003` | User not found | 404 |
| `USER.004` | Failed to sign out | 500 |
| `AUTH.001` | Invalid username/email (user not found) | 401 |
| `AUTH.002` | Invalid password | 401 |
| `AUTH.003` | User account is inactive/pending/etc | 403 |
| `AUTH.004` | Failed to sign in | 500 |
| `AUTH.005` | Token has expired | 401 |
| `AUTH.006` | Invalid token | 401 |

## Security Considerations

### Password Security
- Passwords are hashed using **bcrypt** with 12 rounds of salt
- Plain text passwords are never stored in the database
- Password verification uses constant-time comparison to prevent timing attacks
- Minimum password length: 8 characters

### JWT Token Security
- Tokens are signed with **HS256** algorithm
- Default expiration: 24 hours (configurable)
- Tokens include issued-at (`iat`) and expiration (`exp`) claims
- Should use HTTPS in production to prevent token interception
- **IMPORTANT:** Change `JWT_SECRET_KEY` in production (use environment variables)

### Account Protection
- Email uniqueness validation prevents account enumeration
- User status validation prevents login of inactive accounts
- Session tracking enables logout from all devices
- Last login timestamp for security audits

## Configuration

Update JWT configuration in `_meta/default.py`:

```python
# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24
```

## Usage Examples

### Using with FastAPI

```python
from fastapi import FastAPI, Depends, HTTPException
from ecom_domain.ecom_client import JWTHelper
from typing import Optional

app = FastAPI()

async def get_current_user(token: str = Depends(...)):
    try:
        payload = JWTHelper.verify_token(token)
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.get("/protected")
async def protected_route(user = Depends(get_current_user)):
    return {"message": f"Hello {user['username']}"}
```

### Testing

```python
import asyncio
from ecom_domain.ecom_client import ECOMClientServiceDomain, datadef
from ecom_schema import EcomConnector

async def test_signup():
    domain = ECOMClientServiceDomain()
    
    signup_payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    async with EcomConnector() as stm:
        responses = []
        async for response in domain.process("sign-up", signup_payload):
            responses.append(response)
        
        return responses[-1]

# Run test
result = asyncio.run(test_signup())
print(f"User ID: {result.data['user_id']}")
print(f"Token: {result.data['access_token']}")
```

## Migration Notes

If you have existing users created before implementing this authentication system:

1. Set initial passwords for users using the `hash_password` method
2. Create `UserIdentity` records for existing users with their provider information
3. Ensure all users have `UserSession` records for active sessions
4. Update user profiles if needed

## Future Enhancements

Potential improvements for production:

1. **Refresh Tokens**: Implement token refresh mechanism for extended sessions
2. **Two-Factor Authentication (2FA)**: Add SMS/email verification codes
3. **OAuth Integration**: Support third-party providers (Google, GitHub, etc.)
4. **Rate Limiting**: Implement login attempt rate limiting
5. **IP Whitelisting**: Allow per-session IP tracking and validation
6. **Device Tracking**: Track login devices and locations
7. **Password Reset**: Implement secure password reset flow
8. **Email Verification**: Require email verification before account activation
9. **Audit Logging**: Log all authentication events for security audit  
10. **Token Rotation**: Implement automatic token rotation on refresh

## Troubleshooting

### Issue: "Invalid token" error

**Cause:** Token signature doesn't match or token is corrupted.

**Solution:** Ensure `JWT_SECRET_KEY` is consistent across all instances.

### Issue: "Token has expired" error

**Solution:** Generate a new token by signing in again.

### Issue: "User not found" on login

**Solutions:**
- Check username spelling
- Verify email address is used (emails work as alternative login)
- Check if user was deleted

### Issue: "Invalid password"

**Solution:** Ensure user enters correct password (case-sensitive).

---

**Last Updated:** 2024
**Version:** 1.0
