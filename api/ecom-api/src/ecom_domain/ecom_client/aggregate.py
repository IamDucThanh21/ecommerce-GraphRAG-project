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
    @action("jwt-token-generate", resources="user")
    async def generate_jwt_token(
        self,
        user_id: uuid.UUID,
        username: str,
        session_id: str,
        expires_in_hours: int = JWT_EXPIRATION_HOURS
    ) -> str:

        now = datetime.now(timezone.utc)

        payload = {
            "user_id": str(user_id),
            "username": username,
            "session_id": str(session_id),
            "exp": int((now + timedelta(hours=int(expires_in_hours))).timestamp()),
            "iat": int(now.timestamp()),
            "type": "access",
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

    @action("get-user-identity", resources="user")
    async def get_user_identity(self, username: str):
        """
        Get user identity by username.
        
        Args:
            stm: State manager
            username: Username
            
        Returns:
            UserIdentity object or None
        """
        user = await self.statemgr.find_one(
            "user",
            where={"username": username, "_deleted": None}
        )
        if not user:
            raise ValueError("User not found")
        
        user_identity = await self.statemgr.find_one(
            "user_identity",
            where={"user_id": user._id, "_deleted": None}
        )
        if not user_identity:
            raise ValueError("User identity not found")
        
        return user_identity

    @action("get-user", resources="user")
    async def get_user(self, user_id):
        """
        Get user by ID.
        
        Args:
            stm: State manager
            user_id: User ID
            
        Returns:
            User object or None
        """
        user = await self.statemgr.find_one(
            "user",
            where={"_id": user_id, "_deleted": None}
        )
        if not user:
            raise ValueError("User not found")
        
        return user
        # async with stm.session() as session:
        #     stmt = select(User).where(User._id == user_id)
        #     result = await session.execute(stmt)
        #     return result.scalar_one_or_none()

    @action("create-session", resources="user")
    async def create_session(self, user_id, session_id, source: UserSourceEnum = UserSourceEnum.WEB, email: str = None) -> dict:
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

    @action("update-last-login", resources="user")
    async def update_last_login(self, user_id) -> None:
        """
        Update the last login time for a user.
        
        Args:
            stm: State manager
            user_id: User ID
        """
        profile = await self.statemgr.find_one(
            "profile",
            where={"user_id": user_id, "_deleted": None}
        )
        if profile:
            profile.last_login = datetime.now(timezone.utc)
            await self.statemgr.update(profile)

    @action("check-session", resources="user_session")
    async def check_session(self, session_id, auth_user_id):
        # Fetch the actual session entity from state manager
        session = await self.statemgr.find_one(
            "user_session",
            where={"_id": session_id, "_deleted": None}
        )
        
        if session:
            return True
        else:
            raise BadRequestError("AUTH.007", "Session not found")
        
        # if str(session.user_id) != str(auth_user_id):
        #     raise BadRequestError("AUTH.009", "Unauthorized to invalidate this session.")

        return True

    @action("invalidate-session", resources="user_session")
    async def invalidate_session(self, session_id):
        """
        Invalidate a specific user session.
        
        Args:
            stm: State manager
            session_id: Session ID to invalidate
        """
        session = await self.statemgr.find_one(
            "user_session",
            where={"_id": session_id}
        )

        if not session:
            raise BadRequestError("AUTH.008", "Session not found")

        await self.statemgr.invalidate(session)

        # blacklist the token (Redis)
        # ttl = session.token_exp - int(time.time())  # remaining seconds
        # if ttl > 0:
        #     await redis_client.set(f"revoked:{session.jti}", "1", ex=ttl)

        return session

    @action("invalidate-all-sessions", resources="user_session")
    async def invalidate_all_sessions(self, stm, user_id: uuid.UUID) -> None:
        """
        Invalidate all sessions for a user.
        
        Args:
            stm: State manager
            user_id: User ID
        """

        sessions = await self.statemgr.find_all(
            "user_session", where={"user_id": user_id, "_deleted": None}
        )
        for s in sessions:
            await self.statemgr.invalidate(s)
