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
        try:
            # Parse and validate input
            signup_data = serialize_mapping(payload)
            username = signup_data["username"]
            email = signup_data["email"]
            password = signup_data["password"]
            first_name = signup_data["first_name"]
            last_name = signup_data["last_name"]
            phone = signup_data["phone"]


            # Check if user already exists by username
            existing_user = await agg.check_user_exists(stm, username, email)
            if existing_user:
                raise BadRequestError(
                    "USER.001",
                    "Username or email already registered. Please use a different username or email."
                )

            # Create initial session
            session_id = UUID_GENR()
            new_user_id = UUID_GENR()
            await agg.create_session(
                stm=stm,
                user_id=new_user_id,
                session_id=session_id,
                source=UserSourceEnum.WEB
            )
            
            # Create new user
            user_data = await agg.create_user(
                stm=stm,
                user_id=new_user_id,
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            
            # Generate JWT token
            token = agg.generate_jwt_token(user_id=new_user_id, username=username, session_id=session_id)
            
            
            
            yield agg.create_response(
                status="success",
                message="User registered successfully.",
                data={
                    "user_id": str(new_user_id),
                    "username": username,
                    "email":email,
                    "access_token": token,
                    "token_type": "Bearer",
                    "expires_in": JWT_EXPIRATION_HOURS * 3600,
                    "session_id": str(session_id)
                }
            )
        except BadRequestError:
            raise
        except Exception as e:
            logger.error(f"Sign-up error: {str(e)}")
            raise BadRequestError(
                "USER.002",
                f"Failed to register user: {str(e)}"
            )


class SignInCommand(Command):
    """Command to sign in a user (login)."""

    class Meta:
        key = "sign-in"
        description = "Authenticate a user and provide JWT token."
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
            Data = datadef.SignInData
            signin_data = Data(**serialize_mapping(payload))
            
            # Find user by username or email
            user_identity = await agg.get_user_identity(stm, signin_data.username)
            if not user_identity:
                raise BadRequestError(
                    "AUTH.001",
                    "Invalid username or email. User not found."
                )
            
            # Verify password
            if not agg.verify_password(signin_data.password, user_identity.password_hash):
                raise BadRequestError(
                    "AUTH.002",
                    "Invalid password. Please try again."
                )
            
            # Get user details
            user_id = user_identity.user_id
            user = await agg.get_user(stm, user_id)
            
            # Check user status
            if user.status != UserStatusEnum.ACTIVE:
                raise BadRequestError(
                    "AUTH.003",
                    f"User account is {user.status.value}. Cannot sign in."
                )
            
            # Generate JWT token
            token = agg.generate_jwt_token(user_id=user_id, username=user.username)
            
            # Create session
            session_id = UUID_GENR()
            await agg.create_session(
                stm=stm,
                user_id=user_id,
                session_id=session_id,
                source=UserSourceEnum.WEB,
                email=user_identity.telecom__email
            )
            
            # Update last login
            await agg.update_last_login(stm, user_id)
            
            yield agg.create_response(
                status="success",
                message="Sign in successful.",
                data={
                    "user_id": str(user_id),
                    "username": user.username,
                    "access_token": token,
                    "token_type": "Bearer",
                    "expires_in": JWT_EXPIRATION_HOURS * 3600,
                    "session_id": str(session_id)
                }
            )
        except BadRequestError:
            raise
        except Exception as e:
            logger.error(f"Sign-in error: {str(e)}")
            raise BadRequestError(
                "AUTH.004",
                f"Failed to sign in: {str(e)}"
            )


class LogOutCommand(Command):
    """Command to log out a user."""

    class Meta:
        key = "log-out"
        description = "Invalidate user session and log out."
        resources = ("user",)
        auth_required = True

    async def _process(self, agg, stm, payload):
        """
        Process user logout.
        
        Args:
            agg: Aggregate instance
            stm: State manager
            payload: LogOutData with user_id and optional session_id
        
        Yields:
            Response confirming logout
        """
        try:
            # Parse and validate input
            Data = datadef.LogOutData
            logout_data = Data(**serialize_mapping(payload))
            
            # Verify user exists
            user = await agg.get_user(stm, logout_data.user_id)
            if not user:
                raise BadRequestError(
                    "USER.003",
                    "User not found."
                )
            
            # Invalidate session(s)
            if logout_data.session_id:
                # Logout from specific session
                await agg.invalidate_session(stm, logout_data.session_id)
            else:
                # Logout from all sessions
                await agg.invalidate_all_sessions(stm, logout_data.user_id)
            
            yield agg.create_response(
                status="success",
                message="Sign out successful.",
                data={
                    "user_id": str(logout_data.user_id),
                    "logged_out_at": datetime.now(timezone.utc).isoformat()
                }
            )
        except BadRequestError:
            raise
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            raise BadRequestError(
                "USER.004",
                f"Failed to sign out: {str(e)}"
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
