from fluvius.domain.aggregate import Aggregate, action
from fluvius.data import serialize_mapping, UUID_GENR
from fluvius.data.exceptions import ItemNotFoundError
from fluvius.error import BadRequestError
from sqlalchemy import select, or_
import bcrypt
import jwt
import uuid
from decimal import Decimal

from ecom_schema.ecom_client.user import User, UserIdentity, UserSession
from ecom_schema.ecom_client.profile import Profile
from .types import UserStatusEnum, UserSourceEnum

from . import logger, config
from datetime import datetime, timezone, timedelta, date, time


# JWT Configuration
JWT_SECRET_KEY = config.JWT_SECRET_KEY if hasattr(config, 'JWT_SECRET_KEY') else "your-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


class EcomClientAggregate(Aggregate):
    """Aggregate for ecom client domain."""

    @action("generate-jwt-token", resources="user")
    def generate_jwt_token(
    session_id: str,
    user_id: uuid.UUID,
    username: str,
    expires_in_hours: int = JWT_EXPIRATION_HOURS
    ) -> str:
        payload = {
            "user_id": str(user_id),
            "username": username,
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in_hours),
            "iat": datetime.now(timezone.utc),
            "type": "access",
            "session_id": session_id,
        }

        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    def verify_jwt_token(self, token: str) -> dict:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload
            
        Raises:
            jwt.InvalidTokenError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise BadRequestError("AUTH.005", "Token has expired.")
        except jwt.InvalidTokenError:
            raise BadRequestError("AUTH.006", "Invalid token.")

    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @action
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain text password against its hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password from database
            
        Returns:
            True if password matches, False otherwise
        """
        if not hashed_password:
            return False
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            return False

    @action("check-user-exists", resources="user")
    async def check_user_exists(self, username: str, email: str):
        """
        Check if a user already exists by username or email.
        
        Args:
            stm: State manager
            username: Username to check
            email: Email to check
            
        Returns:
            True if user exists, False otherwise
        """
        existing_user = await self.statemgr.exist(
            "user",
            where={"username": username,"_deleted": None}
        )
        if existing_user:
            return True

        existing_identity = await self.statemgr.exist(
            "user_identity",
            where={"telecom__email": email,"_deleted": None}
        )
        return existing_identity

        # if not existing_user:
        #     existing_user = await self.statemgr.exist(
        #         "user_identity",
        #         where={
        #             "telecom__email": email
        #         }
        #     )
        #     return existing_user

    @action("create-user", resources="user")
    async def create_user(
        self,
        user_id: uuid.UUID,
        username: str,
        email: str,
        password: str,
        first_name: str = None,
        last_name: str = None,
        phone: str = None
    ) -> dict:
        """
        Create a new user with profile and identity.
        
        Args:
            stm: State manager
            user_id: User ID
            username: Username
            email: Email address
            password: Plain text password
            first_name: User's first name
            last_name: User's last name
            phone: User's phone number
            
        Returns:
            Dictionary with user creation details
        """
        hashed_password = self.hash_password(password)
        
        # async with stm.session() as session:
        #     # Create user
        #     user = User(
        #         _id=user_id,
        #         username=username,
        #         active=True,
        #         status=UserStatusEnum.ACTIVE,
        #         is_super_admin=False
        #     )
        #     session.add(user)
            
        #     # Create user identity (local provider)
        #     user_identity = UserIdentity(
        #         _id=UUID_GENR(),
        #         user_id=user_id,
        #         provider="local",
        #         provider_user_id=username,
        #         active=True,
        #         telecom__email=email,
        #         telecom__phone=phone,
        #         password_hash=hashed_password
        #     )
        #     session.add(user_identity)
            
        #     # Create user profile
        #     profile = Profile(
        #         _id=UUID_GENR(),
        #         user_id=user_id,
        #         username=username,
        #         telecom__email=email,
        #         telecom__phone=phone,
        #         name__given=first_name,
        #         name__family=last_name,
        #         verified_email=email if first_name and last_name else None,
        #         status=UserStatusEnum.ACTIVE,
        #         current_profile=True
        #     )
        #     session.add(profile)
            
        #     await session.commit()
            
        #     return {
        #         "user_id": user_id,
        #         "username": username,
        #         "email": email,
        #         "first_name": first_name,
        #         "last_name": last_name,
        #         "phone": phone
        #     }

        user = self.init_resource(
            "user",
            _id=user_id,
            username=username,
            active=True,
            status=UserStatusEnum.ACTIVE.value,
            is_super_admin=False
        )
        await self.statemgr.insert(user)

        user_identity = self.init_resource(
            "user_identity",
            _id=UUID_GENR(),
            user_id=user_id,
            provider="local",
            provider_user_id=username,
            active=True,
            telecom__email=email,
            telecom__phone=phone,
            password_hash=hashed_password
        )
        await self.statemgr.insert(user_identity)

        profile = self.init_resource(
            "profile",
            _id=UUID_GENR(),
            user_id=user_id,
            username=username,
            telecom__email=email,
            telecom__phone=phone,
            name__given=first_name,
            name__family=last_name,
            verified_email=email if first_name and last_name else None,
            status=UserStatusEnum.ACTIVE.value,
            current_profile=True
        )
        await self.statemgr.insert(profile)

        return {
            "user_id": user_id,
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone
        }

    @action
    async def get_user_identity(self, stm, username_or_email: str) -> UserIdentity:
        """
        Get user identity by username or email.
        
        Args:
            stm: State manager
            username_or_email: Username or email address
            
        Returns:
            UserIdentity object or None
        """
        async with stm.session() as session:
            # First try to find by email
            stmt = select(UserIdentity).where(UserIdentity.telecom__email == username_or_email)
            result = await session.execute(stmt)
            identity = result.scalar_one_or_none()
            
            if not identity:
                # Try to find by username (through user relationship)
                stmt = select(UserIdentity).join(User).where(User.username == username_or_email)
                result = await session.execute(stmt)
                identity = result.scalar_one_or_none()
            
            return identity

    @action
    async def get_user(self, stm, user_id: uuid.UUID) -> User:
        """
        Get user by ID.
        
        Args:
            stm: State manager
            user_id: User ID
            
        Returns:
            User object or None
        """
        async with stm.session() as session:
            stmt = select(User).where(User._id == user_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @action("create-session", resources="user")
    async def create_session(self, user_id: uuid.UUID, session_id: uuid.UUID, source: UserSourceEnum = UserSourceEnum.WEB, email: str = None) -> dict:
        """
        Create a user session.
        
        Args:
            stm: State manager
            user_id: User ID
            session_id: Session ID
            source: Source of the session
            email: Email associated with session
            
        Returns:
            Dictionary with session details
        """
        # async with stm.session() as session:
        #     user_session = UserSession(
        #         _id=session_id,
        #         user_id=user_id,
        #         source=source,
        #         telecom__email=email,
        #         user_identity_id=None
        #     )
        #     session.add(user_session)
        #     await session.commit()
            
        #     return {
        #         "session_id": session_id,
        #         "user_id": user_id,
        #         "source": source.value if source else None
        #     }
        user_session = self.init_resource(
            "user_session",
            _id=session_id,
            user_id=user_id,
            source=source,
            telecom__email=email
        )

        await self.statemgr.insert(user_session)
        return {
            "session_id": session_id,
            "user_id": user_id,
            "source": source.value if source else None
        }

    @action
    async def update_last_login(self, stm, user_id: uuid.UUID) -> None:
        """
        Update the last login time for a user.
        
        Args:
            stm: State manager
            user_id: User ID
        """
        async with stm.session() as session:
            stmt = select(Profile).where(Profile.user_id == user_id)
            result = await session.execute(stmt)
            profile = result.scalar_one_or_none()
            
            if profile:
                profile.last_login = datetime.now(timezone.utc)
                await session.commit()

    @action
    async def invalidate_session(self, stm, session_id: uuid.UUID) -> None:
        """
        Invalidate a specific user session.
        
        Args:
            stm: State manager
            session_id: Session ID to invalidate
        """
        async with stm.session() as session:
            stmt = select(UserSession).where(UserSession._id == session_id)
            result = await session.execute(stmt)
            user_session = result.scalar_one_or_none()
            
            if user_session:
                await session.delete(user_session)
                await session.commit()

    @action
    async def invalidate_all_sessions(self, stm, user_id: uuid.UUID) -> None:
        """
        Invalidate all sessions for a user.
        
        Args:
            stm: State manager
            user_id: User ID
        """
        async with stm.session() as session:
            stmt = select(UserSession).where(UserSession.user_id == user_id)
            result = await session.execute(stmt)
            sessions = result.scalars().all()
            
            for user_session in sessions:
                await session.delete(user_session)
            
            await session.commit()
