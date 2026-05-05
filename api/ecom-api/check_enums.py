#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, 'src')

try:
    from ecom_schema import config as ecom_config
    from sqlalchemy import create_engine, text

    # Create engine
    engine = create_engine(ecom_config.DB_DSN.replace('+asyncpg://', '+psycopg2://'))

    with engine.connect() as conn:
        # Check for enum types in ecom_product schema
        result = conn.execute(text("""
            SELECT n.nspname as schema_name, t.typname as type_name, e.enumlabel as enum_value
            FROM pg_type t
            JOIN pg_namespace n ON n.oid = t.typnamespace
            JOIN pg_enum e ON e.enumtypid = t.oid
            WHERE n.nspname = 'ecom_product'
            ORDER BY n.nspname, t.typname, e.enumsortorder
        """))

        print("Enum types in ecom_product schema:")
        found = False
        for row in result:
            found = True
            print(f"  {row.schema_name}.{row.type_name}: {row.enum_value}")

        if not found:
            print("  No enum types found in ecom_product schema")

        # Also check default schema
        result = conn.execute(text("""
            SELECT n.nspname as schema_name, t.typname as type_name, e.enumlabel as enum_value
            FROM pg_type t
            JOIN pg_namespace n ON n.oid = t.typnamespace
            JOIN pg_enum e ON e.enumtypid = t.oid
            WHERE n.nspname = 'public'
            ORDER BY n.nspname, t.typname, e.enumsortorder
        """))

        print("\nEnum types in public schema:")
        found = False
        for row in result:
            found = True
            print(f"  {row.schema_name}.{row.type_name}: {row.enum_value}")

        if not found:
            print("  No enum types found in public schema")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()