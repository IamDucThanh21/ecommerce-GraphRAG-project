from enum import Enum

class ResourceTypeEnum(str, Enum):
    PRODUCT = "product"
    POST = "post"

class ReactionTypeEnum(str, Enum):
    LIKE = "like"
    LOVE = "love"
    HAHA = "haha"
    SAD = "sad"
    WOW = "wow"
    ANGRY = "angry"
