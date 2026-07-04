from typing import Optional
from uuid import UUID, uuid4
from fastapi import Request
from fluvius.fastapi.auth import (FluviusAuthProfileProvider,)
from fluvius.auth import (AuthorizationContext,SessionProfile,SessionOrganization,KeycloakTokenPayload,)
from fluvius.error import (UnauthorizedError,)
from fluvius.data import (DataAccessManager,)
from ecom_domain.ecom_client.jwt_helper import JWTHelper
from ecom_schema import (EcomConnector,)

class JWTAuthProvider(
    FluviusAuthProfileProvider,
    DataAccessManager
):
    """
    JWT authentication provider
    using local HS256 JWT instead of Keycloak.

    Reuses Fluvius AuthorizationContext
    so auth_required=True continues to work.
    """

    __connector__ = EcomConnector
    __automodel__ = True

    DEFAULT_ROLE = "user"
    DEFAULT_REALM = "local"

    def __init__(self, app):
        FluviusAuthProfileProvider.__init__(self,app)

        DataAccessManager.__init__(self,app=app)

    def get_auth_token(self, request: Request) -> Optional[dict]:
        """
        Extract JWT from Authorization header
        and return decoded payload.
        """

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        if not auth_header.startswith("Bearer "):
            raise UnauthorizedError("AUTH.INVALID_HEADER","Authorization header must use Bearer token.")

        token = auth_header[7:].strip()
        if not token:
            raise UnauthorizedError("AUTH.EMPTY_TOKEN", "Access token is missing.")

        try:
            payload = JWTHelper.verify_token(token)
            if not isinstance(payload, dict):
                raise UnauthorizedError("AUTH.INVALID_PAYLOAD", "JWT payload must be a dictionary.")
            return payload

        except UnauthorizedError:
            raise
        except Exception as e:
            raise UnauthorizedError(
                "AUTH.INVALID_TOKEN",
                f"Access token is invalid: {str(e)}"
            )

    async def get_auth_context(self, request: Request, **kwargs) -> Optional[AuthorizationContext]:
        """
        Build Fluvius AuthorizationContext
        from local JWT payload.
        """

        payload = self.get_auth_token(request)

        # Guest access allowed
        if not payload:
            return None
        
        headers = dict(request.headers)

        user_id = payload.get("user_id")
        if not user_id:
            raise UnauthorizedError("AUTH.NO_USER_ID", "user_id missing in token.")
        try:
            user_uuid = UUID(str(user_id))
        except (ValueError,TypeError):
            raise UnauthorizedError("AUTH.INVALID_USER_ID", "Invalid user_id format.")

        # ------------------------------------------------
        # Fetch user from DB
        # ------------------------------------------------
        async with self.transaction():
            user = await self.fetch("user",user_uuid)
        if not user:
            raise UnauthorizedError("AUTH.USER_NOT_FOUND", "User not found.")

        # ------------------------------------------------
        # Safe field extraction
        # ------------------------------------------------
        username = (getattr(user,"username",None) or payload.get("username") or "")
        first_name = (getattr(user,"first_name",None) or "")
        last_name = (getattr(user,"last_name",None) or "")
        email = (getattr(user,"email",None) or "guest@example.com")
        is_super_admin = bool(getattr(user, "is_super_admin", False))
        roles = ("admin", "user") if is_super_admin else ("user",)
        role = (payload.get("role") or self.DEFAULT_ROLE)

        session_id = payload.get("session_id")

        try:
            session_uuid = (session_id if session_id else None)
        except (ValueError,TypeError):
            raise UnauthorizedError("AUTH.INVALID_SESSION_ID", "Invalid session_id format.")

        # ------------------------------------------------
        # Mimic Keycloak payload
        # Required by Fluvius
        # ------------------------------------------------
        auth_user = (
            KeycloakTokenPayload(exp=payload.get("exp",9999999999),
                iat=payload.get("iat",0),
                auth_time=payload.get("iat",0),
                # safer than user._id
                jti=str(uuid4()),
                iss="http://localhost",
                aud="ecommerce-api",
                sub=user._id,
                typ="Bearer",
                azp="ecommerce-api",
                sid=session_uuid,
                email_verified=bool(email),
                name=username,
                preferred_username=username,
                given_name=first_name,
                family_name=last_name,
                email=email,
                phone=None,
                realm_access={"roles": list(roles)},
                resource_access={},
                session_id=session_uuid,
                client_token=None,
            )
        )

        profile = SessionProfile(
            id=user._id,
            name=username,
            family_name=last_name,
            given_name=first_name,
            email=email,
            username=username,
            roles=roles,
            org_id=None,
            usr_id=user._id,
        )

        organization = (
            SessionOrganization(
                id=user._id,
                name=self.DEFAULT_REALM
            )
        )

        # ------------------------------------------------
        # Final auth context
        # ------------------------------------------------

        # print(type(auth_user))
        # print(auth_user)
        # print(type(profile))
        # print(profile)
        # print(type(organization))
        # print(organization)

        # ctx = AuthorizationContext(
        #     realm="local",
        #     user=auth_user,
        #     profile=profile,
        #     organization=organization,
        #     iamroles=("user",)
        # )

        # print(type(ctx))
        # print(ctx)

        # print(ctx.model_dump())
        return AuthorizationContext(
            realm=self.DEFAULT_REALM,
            user=auth_user,
            profile=profile,
            organization=organization,
            iamroles=roles,
            headers=headers
        )