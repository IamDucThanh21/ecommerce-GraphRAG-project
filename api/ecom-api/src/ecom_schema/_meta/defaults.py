MAX_MUTATIONS = 50
# Database Configuration
DB_DSN = "postgresql+asyncpg://ecommerce:123456@localhost:5432/ecommerce"
DB_SCHEMA = "ecom_schema"


# import os

# LOG_LEVEL = os.environ.get("LOG_LEVEL")
# DB_DSN = os.environ.get("PRODUCT_DB_DSN") or os.environ.get("DB_DSN") or "postgresql://localhost/ecommerce"
# DB_SCHEMA = os.environ.get("PRODUCT_SCHEMA", "product")
# PRODUCT_NAMESPACE = "product"