from enum import Enum

class ConversationStatusEnum(Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
 
 
class MessageRoleEnum(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
 
 
class MessageIntentEnum(Enum):
    PRODUCT_SEARCH = "product_search"
    COMPARE = "compare"
    CLARIFY = "clarify"
    SMALL_TALK = "smalltalk"
 
 
class ProductStatusEnum(Enum):
    ACTIVE = "active"
    DISCONTINUED = "discontinued"
    OUT_OF_STOCK = "out_of_stock"
 
 
class RecommendationStrategyEnum(Enum):
    RULE_BASED = "rule_based"
    AI_RANKED = "ai_ranked"
    HYBRID = "hybrid"
 
 
class FeedbackActionEnum(Enum):
    VIEWED = "viewed"
    CLICKED = "clicked"
    PURCHASED = "purchased"
    DISMISSED = "dismissed"
    HELPFUL = "helpful"
    NOT_HELPFUL = "not_helpful"
 
 
class DomainAggregateTypeEnum(Enum):
    CONVERSATION = "Conversation"
    RECOMMENDATION = "Recommendation"
    PRODUCT = "Product"