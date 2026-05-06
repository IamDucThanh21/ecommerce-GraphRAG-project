from datetime import datetime, timedelta, timezone
from fluvius.data import serialize_mapping, UUID_GENR
from fluvius.error import BadRequestError
from .domain import ECOMClientServiceDomain
from ecom_schema.ecom_client.types import UserStatusEnum, UserSourceEnum

from . import datadef
from . import config, logger
import secrets
import uuid
import bcrypt
import jwt
from typing import Optional

Command = ECOMClientServiceDomain.Command

# JWT Configuration
JWT_SECRET_KEY = "your-secret-key-change-in-production"  # Should come from environment
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


class SignUpCommand(Command):
    """Command to sign up a new user."""

    Data = datadef.SignUpData

    class Meta:
        key = "sign-up"
        description = "Register a new user account in the system."
        resources = ("user",)
        resource_init = True
        auth_required = False

    async def _process(self, agg, stm, payload):
        """
        Process user sign-up.
        
        Args:
            agg: Aggregate instance
            stm: State manager
            payload: SignUpData with username, email, password, first_name, last_name, phone
        
        Yields:
            Response with user_id, username, email, and JWT token
        """

        # Parse and validate input
        signup_data = serialize_mapping(payload)
        username = signup_data["username"]
        email = signup_data["email"]
        password = signup_data["password"]
        first_name = signup_data["first_name"]
        last_name = signup_data["last_name"]
        phone = signup_data["phone"]    
        existing_user = await agg.check_user_exists(username=username, email=email)
        if existing_user:
            raise BadRequestError(
                    "USER.001",
                    "Username or email already registered. Please use a different username or email."
                )
        
        # Create user first (before session, due to FK constraint)
        new_user_id = UUID_GENR()
        user_data = await agg.create_user(
            user_id=new_user_id,
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        
        # Create session after user exists
        session_id = UUID_GENR()
        await agg.create_session(
            user_id=new_user_id,
            session_id=session_id,
            source=UserSourceEnum.WEB
        )
        
        # Generate JWT token
        token = await agg.generate_jwt_token(new_user_id, username)
        
        response_data = {
            "user_id": str(new_user_id),
            "username": username,
            "email": email,
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": JWT_EXPIRATION_HOURS * 3600,
            "session_id": str(session_id)
        }
        
        yield agg.create_response(
            response_data,
            _type="user-signup-response"
        )


class SignInCommand(Command):
    """Command to sign in a user (login)."""

    Data = datadef.SignInData

    class Meta:
        key = "sign-in"
        description = "Authenticate a user and provide JWT token."
        resource_init = True
        resources = ("user",)
        auth_required = False
        
    async def _process(self, agg, stm, payload):
        """
        Process user sign-in (login).
        
        Args:
            agg: Aggregate instance
            stm: State manager
            payload: SignInData with username and password
        
        Yields:
            Response with JWT token and session information
        """
        try:
            # Parse and validate input
            signin_data = serialize_mapping(payload)
            
            # Find user by username or email
            user_identity = await agg.get_user_identity(username=signin_data["username"])
            if not user_identity:
                raise BadRequestError(
                    "AUTH.001",
                    "Invalid username or email. User not found."
                )
            
            # Verify password
            hash_password = user_identity.password_hash
            verify_result = bcrypt.checkpw(signin_data["password"].encode('utf-8'), hash_password.encode('utf-8'))
            
            if not verify_result:
                raise BadRequestError(
                    "AUTH.002",
                    "Invalid password. Please try again."
                )
            
            user = await agg.get_user(user_id=user_identity.user_id)
            # Check user status
            if user.status != UserStatusEnum.ACTIVE:
                raise BadRequestError(
                    "AUTH.003",
                    f"User account is {user.status.value}. Cannot sign in."
                )
            
            # Generate JWT token
            # token = await agg.generate_jwt_token(user_id=user._id, username=user.username)
            now = datetime.now(timezone.utc)

            payload = {
                "user_id": str(user._id),
                "username": user.username,
                "exp": int((now + timedelta(hours=int(JWT_EXPIRATION_HOURS))).timestamp()),
                "iat": int(now.timestamp()),
                "type": "access",
            }

            token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
            # Create session
            session_id = UUID_GENR()
            await agg.create_session(
                user_id=user._id,
                session_id=session_id,
                source=UserSourceEnum.WEB,
                email=user_identity.telecom__email
            )
            
            # Update last login
            await agg.update_last_login(user_id=user._id)
            response_data = {
                "user_id": str(user._id),
                "username": user.username,
                "access_token": str(token),
                "token_type": "Bearer",
                "expires_in": int(JWT_EXPIRATION_HOURS) * 3600,
                "session_id": str(session_id)
            }
            yield agg.create_response(
                status="success",
                message="Sign-in successful",
                data=response_data,
                _type="user-signin-response"
            )
        except BadRequestError:
            raise
        except Exception as e:
            logger.error(f"Sign-in error: {str(e)}")
            raise BadRequestError(
                "AUTH.004",
                f"Failed to sign in: {str(e)}"
            )


class SignOutCommand(Command):
    """Command to log out a user."""

    class Meta:
        key = "sign-out"
        description = "Invalidate user session and log out."
        resources = ("user_session",)
        tags = ["user", "session", "auth"]
        auth_required = True

    async def _process(self, agg, stm, payload):
        """
        Process user logout.
        
        Args:
            agg: Aggregate instance
            stm: State manager
            payload: Empty or with additional data
        
        Yields:
            Response confirming logout
        """
        session_id = agg.get_aggroot().identifier
        auth_user_id = agg.get_context().user_id
        
        # Fetch the actual session entity from state manager
        # session = await stm.find_one(
        #     "user_session",
        #     where={"_id": session_id, "_deleted": None}
        # )
        
        # if not session:
        #     raise BadRequestError("AUTH.007", "Session not found")
        
        # session_owner_id = session.user_id
        
        # print(f"Session ID: {session_id}")
        # # print(f"Session owner (from DB): {session_owner_id}")
        # print(f"Auth user (from JWT context): {auth_user_id}")
        # # print(f"Session object: {session}")
        # print(f"Auth context user_id: {agg.get_context().user_id}")
        session = await agg.invalidate_session(session_id=session_id)
        
        response_data = {
            "user_id": str(session.user_id),
            "session_id": str(session_id),
            "logged_out_at": datetime.now(timezone.utc).isoformat()
        }
        
        yield agg.create_response(
            response_data,
            _type="user-logout-response"
        )


class CreateUserCommand(Command):
    """Command to create a new user (legacy)."""

    class Meta:
        key = "create-new-user"
        description = "Command to create a new user in the system."
        resources = ("user",)
        resource_init = True
        auth_required = False

    async def _process(self, agg, stm, payload):
        username = "Đức Thành"

        yield agg.create_response(
            status="success",
            message="User created successfully.",
            data={
                "username": username
            }
        )

    