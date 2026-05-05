import os
from ecom_schema._meta import logger
from . import SCHEMA


from alembic_utils.pg_view import PGView
from alembic_utils.replaceable_entity import register_entities

# ─────────────────────────────────────────────────────────────────────────────
# VIEW 1 — Category list
# Returns: all categories with brand count and brand name array
# Usage: Level 1 navigation (category picker)
# ─────────────────────────────────────────────────────────────────────────────
product_category_list_view = PGView(
    schema=SCHEMA,
    signature="_product_category_list",
    definition=f"""
    SELECT
        pc._id,
        pc._created,
        pc._updated,
        pc._creator,
        pc._updater,
        pc._deleted,
        pc._etag,
        pc._realm,
        pc.name,
        pc.description,
        (
            SELECT COUNT(DISTINCT pl.brand_id)
            FROM "{SCHEMA}".product_line AS pl
            WHERE pl.category_id = pc._id
              AND pl._deleted IS NULL
        )                                                   AS brand_count,
        (
            SELECT COALESCE(
                array_agg(DISTINCT pb.name ORDER BY pb.name),
                ARRAY[]::varchar[]
            )
            FROM "{SCHEMA}".product_line AS pl
            JOIN "{SCHEMA}".product_brand AS pb
                ON pb._id = pl.brand_id
               AND pb._deleted IS NULL
            WHERE pl.category_id = pc._id
              AND pl._deleted IS NULL
        )                                                   AS brand_names
    FROM "{SCHEMA}".product_category AS pc
    WHERE pc._deleted IS NULL
    ORDER BY pc.name;
    """
)
 
 
# ─────────────────────────────────────────────────────────────────────────────
# VIEW 2 — Brand + product line list (by category)
# Returns: one row per (brand, product_line) pair
# Usage: Level 2 navigation — filter by category_id on the application side
# ─────────────────────────────────────────────────────────────────────────────
product_brand_line_list_view = PGView(
    schema=SCHEMA,
    signature="_product_brand_line_list",
    definition=f"""
    SELECT
        pb._id,                  
        pb.name,                
        pb.description,        
        pb._realm,               
        pb._created,           
        pb._updated,           
        pb._etag,                
        pl._id                  AS line_id,
        pl.name                 AS line_name,
        pl.category_id,
        pc.name                 AS category_name,
        pl._created             AS line_created,
        pl._updated             AS line_updated,
        pl._etag                AS line_etag,
        (
            SELECT COUNT(*)
            FROM "{SCHEMA}".product AS p
            WHERE p.line_id = pl._id
              AND p._deleted IS NULL
        )                       AS product_count
    FROM "{SCHEMA}".product_brand AS pb
    JOIN "{SCHEMA}".product_line AS pl
        ON pl.brand_id = pb._id
        AND pl._deleted IS NULL
    JOIN "{SCHEMA}".product_category AS pc
        ON pc._id = pl.category_id
        AND pc._deleted IS NULL
    WHERE pb._deleted IS NULL
    ORDER BY pb.name, pl.name;
    """
)
 
 
# ─────────────────────────────────────────────────────────────────────────────
# VIEW 3 — Product list (card view)
# Returns: one row per product with primary image and active sale price
# Usage: Level 2 product grid — filter by line_id or brand_id
# ─────────────────────────────────────────────────────────────────────────────
product_list_view = PGView(
    schema=SCHEMA,
    signature="_product_list",
    definition=f"""
    SELECT
        p._id,
        p._created,
        p._updated,
        p._creator,
        p._updater,
        p._deleted,
        p._etag,
        p._realm,
        p.name,
        p.description,
        p.status,
        p.line_id,
        pl.name                                             AS line_name,
        pl.brand_id                                         AS brand_id,
        pb.name                                             AS brand_name,
        pl.category_id                                      AS category_id,
        pc.name                                             AS category_name,
        p.base_price,
        pv.price,
        pv.sku,
        pv.stock_quantity,
        CASE
            WHEN pr.discount_percent IS NOT NULL
            THEN ROUND(p.base_price * (1.0 - pr.discount_percent / 100.0), 0)
            ELSE p.base_price
        END                                                 AS sale_price,
        pr.discount_percent,
        pr.gift,
        pr.valid_from                                       AS promo_valid_from,
        pr.valid_to                                         AS promo_valid_to,
        pi.image_url                                        AS primary_image_url
    FROM "{SCHEMA}".product AS p
    JOIN "{SCHEMA}".product_line AS pl
        ON pl._id = p.line_id
        AND pl._deleted IS NULL
    JOIN "{SCHEMA}".product_brand AS pb
        ON pb._id = pl.brand_id
        AND pb._deleted IS NULL
    JOIN "{SCHEMA}".product_category AS pc
        ON pc._id = pl.category_id
        AND pc._deleted IS NULL
    LEFT JOIN "{SCHEMA}".product_variant AS pv
        ON pv.product_id = p._id
        AND pv._deleted IS NULL
    LEFT JOIN "{SCHEMA}".product_image AS pi
        ON pi.product_id = p._id
        AND pi.is_primary = TRUE
        AND pi._deleted IS NULL
    LEFT JOIN "{SCHEMA}".promotion AS pr
        ON pr.product_id = p._id
        AND NOW() BETWEEN pr.valid_from AND pr.valid_to
        AND pr._deleted IS NULL
    WHERE p._deleted IS NULL;
    """
)
 
 
# ─────────────────────────────────────────────────────────────────────────────
# VIEW 4 — Product detail (full info + all images + variants)
# Returns: one row per product variant with all product metadata and images
# Usage: Level 3 product detail page
# ─────────────────────────────────────────────────────────────────────────────
product_detail_view = PGView(
    schema=SCHEMA,
    signature="_product_detail",
    definition=f"""
    SELECT
        p._id,                                               
        p._created,
        p._updated,
        p._creator,
        p._updater,
        p._deleted,
        p._etag,
        p._realm,
        p.name,
        p.description,
        p.status,
        p.llm_spec_text,
        p.line_id,
        pl.name                                             AS line_name,
        pl.brand_id,
        pb.name                                             AS brand_name,
        pb.description                                      AS brand_description,
        pl.category_id,
        pc.name                                             AS category_name,
        pv._id                                              AS variant_id,
        pv.sku,
        p.base_price,
        pv.price,
        pv.stock_quantity,
        pv.attributes                                       AS variant_attributes,
        CASE
            WHEN pr.discount_percent IS NOT NULL
            THEN ROUND(p.base_price * (1.0 - pr.discount_percent / 100.0), 0)
            ELSE p.base_price
        END                                                 AS sale_price,
        pr.discount_percent,
        pr.gift,
        pr.valid_from                                       AS promo_valid_from,
        pr.valid_to                                         AS promo_valid_to,
        COALESCE(img.images, ARRAY[]::json[])               AS images,
        psf.specs_json
    FROM "{SCHEMA}".product AS p
    JOIN "{SCHEMA}".product_line AS pl
        ON pl._id = p.line_id
        AND pl._deleted IS NULL
    JOIN "{SCHEMA}".product_brand AS pb
        ON pb._id = pl.brand_id
        AND pb._deleted IS NULL
    JOIN "{SCHEMA}".product_category AS pc
        ON pc._id = pl.category_id
        AND pc._deleted IS NULL
    LEFT JOIN "{SCHEMA}".product_variant AS pv
        ON pv.product_id = p._id
        AND pv._deleted IS NULL
    LEFT JOIN "{SCHEMA}".promotion AS pr
        ON pr.product_id = p._id
        AND NOW() BETWEEN pr.valid_from AND pr.valid_to
        AND pr._deleted IS NULL
    LEFT JOIN (
        SELECT
            product_id,
            array_agg(
                json_build_object(
                    'image_url',  image_url,
                    'is_primary', is_primary
                ) ORDER BY is_primary DESC, _created ASC
            ) AS images
        FROM "{SCHEMA}".product_image
        WHERE _deleted IS NULL
        GROUP BY product_id
    ) AS img
        ON img.product_id = p._id
    LEFT JOIN "{SCHEMA}".product_spec_flat AS psf
        ON psf.product_id = p._id
        AND psf._deleted IS NULL
    WHERE p._deleted IS NULL;
    """
)
 
 
# ─────────────────────────────────────────────────────────────────────────────
# VIEW 5 — Product specification (grouped)
# Returns: one row per spec attribute value, ordered by group/attr sort_order
# Usage: Level 3 spec table — filter by product_id
# ─────────────────────────────────────────────────────────────────────────────
product_spec_detail_view = PGView(
    schema=SCHEMA,
    signature="_product_spec_detail",
    definition=f"""
    SELECT
        psv._id,                 
        psv._created,
        psv._updated,
        psv._etag,
        psv._realm,
        psv.product_id,
        p.name                  AS product_name,
        sg._id                  AS group_id,
        sg.name                 AS group_name,
        sg.sort_order           AS group_sort_order,
        sg.category_id,
        sa._id                  AS attribute_id,
        sa.name                 AS attribute_name,
        sa.data_type,
        sa.unit,
        sa.sort_order           AS attribute_sort_order,
        psv.value_text,
        psv.value_number,
        psv.value_boolean,
        psv.value_json,
        CASE sa.data_type::text
            WHEN 'TEXT'        THEN psv.value_text
            WHEN 'NUMBER'      THEN CONCAT(psv.value_number::text, ' ', sa.unit)
            WHEN 'BOOLEAN'     THEN CASE WHEN psv.value_boolean THEN 'Có' ELSE 'Không' END
            WHEN 'JSON'        THEN psv.value_json::text
            WHEN 'SELECT'      THEN psv.value_text
            WHEN 'MULTISELECT' THEN psv.value_text
            ELSE NULL
        END                     AS display_value 
    FROM "{SCHEMA}".product_spec_value AS psv
    JOIN "{SCHEMA}".product AS p
        ON p._id = psv.product_id
        AND p._deleted IS NULL
    JOIN "{SCHEMA}".spec_attribute AS sa
        ON sa._id = psv.attribute_id
        AND sa._deleted IS NULL
    JOIN "{SCHEMA}".spec_group AS sg
        ON sg._id = sa.group_id
        AND sg._deleted IS NULL
    WHERE psv._deleted IS NULL
    ORDER BY sg.sort_order, sa.sort_order;
    """
)
 
 
# ─────────────────────────────────────────────────────────────────────────────
# VIEW 6 — Customer review list
# Returns: all reviews per product
# Usage: Level 3 review section — filter by product_id
# ─────────────────────────────────────────────────────────────────────────────
product_review_list_view = PGView(
    schema=SCHEMA,
    signature="_product_review_list",
    definition=f"""
    SELECT
        cr._id,
        cr._created,
        cr._updated,
        cr._creator,
        cr._updater,
        cr._deleted,
        cr._etag,
        cr._realm,
        cr.product_id,
        p.name                  AS product_name,
        cr.customer_name,
        cr.rating,
        cr.comment,
        cr.review_date
    FROM "{SCHEMA}".customer_review AS cr
    JOIN "{SCHEMA}".product AS p
        ON p._id = cr.product_id
        AND p._deleted IS NULL
    WHERE cr._deleted IS NULL
    ORDER BY cr.review_date DESC;
    """
)


def register_pg_entities(allow_flag):
    if not allow_flag:
        logger.info('REGISTER_PG_ENTITIES is disabled or not set.')
        return
    logger.info('Registering PG entities for ecom_product')
    register_entities([
        product_category_list_view,
        product_brand_line_list_view,
        product_list_view,
        product_detail_view,
        product_spec_detail_view,
        product_review_list_view,
    ])


register_pg_entities(os.environ.get('REGISTER_PG_ENTITIES'))