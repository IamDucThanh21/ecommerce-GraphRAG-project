# Aggregate Actions & Command Serialization Updates

## Summary of Changes

Updated the authentication system to follow Fluvius domain-driven design patterns:

### 1. Aggregate Methods with @action Decorator

Added `@action` decorator to all aggregate methods that are called by command handlers:

#### Authentication Methods
- `@action def generate_jwt_token()` - Generate JWT tokens
- `@action def hash_password()` - Hash passwords using bcrypt
- `@action def verify_password()` - Verify password hashes

#### User Management Methods
- `@action async def check_user_exists()` - Check username/email uniqueness
- `@action async def create_user()` - Create user with profile and identity
- `@action async def get_user()` - Retrieve user by ID
- `@action async def get_user_identity()` - Retrieve user identity by username/email

#### Session Management Methods
- `@action async def create_session()` - Create user session
- `@action async def update_last_login()` - Update last login timestamp
- `@action async def invalidate_session()` - Invalidate specific session
- `@action async def invalidate_all_sessions()` - Invalidate all user sessions

### 2. Command Payload Serialization

Updated all command handlers to use proper payload serialization:

#### Pattern Applied
```python
# Create reference to data model
Data = datadef.SignUpData

# Deserialize and validate payload
data = Data(**serialize_mapping(payload))
```

#### Updated Commands
- **SignUpCommand**: `Data = datadef.SignUpData` + `Data(**serialize_mapping(payload))`
- **SignInCommand**: `Data = datadef.SignInData` + `Data(**serialize_mapping(payload))`
- **LogOutCommand**: `Data = datadef.LogOutData` + `Data(**serialize_mapping(payload))`

### Benefits

✅ **Command Pattern Consistency**
- Follows Fluvius domain architecture standards
- Clear separation between payload and business logic
- Proper type validation at command boundary

✅ **Action Tracking**
- `@action` decorator enables event sourcing
- Audit trail of all state-changing operations
- Better command/event separation

✅ **Payload Serialization**
- `serialize_mapping()` provides consistent deserialization
- Proper validation through Pydantic models
- Clear data flow: payload → serialization → domain model

### File Changes

**Modified Files:**
1. `api/ecom-api/src/ecom_domain/ecom_client/aggregate.py`
   - Added 11 `@action` decorators to methods

2. `api/ecom-api/src/ecom_domain/ecom_client/command.py`
   - Updated SignUpCommand._process()
   - Updated SignInCommand._process()
   - Updated LogOutCommand._process()

### Code Flow Example

```python
# Command receives raw payload
await domain.process("sign-up", {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
})

# Inside SignUpCommand._process():
Data = datadef.SignUpData                    # 1. Reference data model
signup_data = Data(**serialize_mapping(payload))  # 2. Deserialize and validate

# Then use aggregate actions
await agg.check_user_exists(stm, signup_data.username, signup_data.email)
await agg.create_user(stm, user_id, ...)
new_token = agg.generate_jwt_token(...)      # @action marked methods
await agg.create_session(stm, ...)
```

### Validation Features

The Pydantic models in datadef.py ensure:
- **SignUpData**: username (3-255), email (valid format), password (≥8 chars), optional names/phone
- **SignInData**: username (3-255), password (required)
- **LogOutData**: user_id (UUID), session_id (optional UUID)

All validation happens at the command boundary before business logic execution.

### Best Practices Applied

1. ✅ **Separation of Concerns**: Payload handling separate from domain logic
2. ✅ **Type Safety**: Pydantic validation with proper error messages
3. ✅ **Event Sourcing Ready**: @action decorators for audit trails
4. ✅ **Consistency**: All commands follow same pattern
5. ✅ **Testability**: Clear, isolated action methods

### Testing

All files pass syntax validation:
```bash
python3 -m py_compile \
  api/ecom-api/src/ecom_domain/ecom_client/command.py \
  api/ecom-api/src/ecom_domain/ecom_client/aggregate.py \
# ✓ No errors
```

---

**Last Updated:** 2024
**Pattern:** Fluvius Domain-Driven Design
