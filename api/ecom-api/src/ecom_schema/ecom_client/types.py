from enum import Enum

class UserStatusEnum(str, Enum):
    """User account status across the system."""
    ACTIVE      = "ACTIVE"
    INACTIVE    = "INACTIVE"
    EXPIRED     = "EXPIRED"
    PENDING     = "PENDING"
    DEACTIVATED = "DEACTIVATED"
    NEW         = "NEW"

class UserSourceEnum(str, Enum):
    """Source system or method of user authentication."""
    WEB       = "WEB"
    MOBILE    = "MOBILE"
    KEYCLOAK  = "KEYCLOAK"
    MOBILE_KC = "MOBILE_KC"
    DASHBOARD  = "DASHBOARD"
    WEBSITE = "WEBSITE"

# class UserRoleEnum(Enum):
#     ADMIN = "ADMIN"
#     CLIENT = "CLIENT"
#     GUEST = "GUEST"