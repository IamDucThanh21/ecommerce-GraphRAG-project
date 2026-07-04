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
# product_category_list_view = PGView(
#     schema=SCHEMA,
#     signature="_product_category_list",
#     definition=f"""
#     SELECT
#         pc._id,
#         pc._created,
#         pc._updated,
#         pc._creator,
#         pc._updater,
#         pc._deleted,
#         pc._etag,
#         pc._realm,
#         pc.name,
#         pc.description,
#         (
#             SELECT COUNT(DISTINCT pl.brand_id)
#             FROM "{SCHEMA}".product_line AS pl
#             WHERE pl.category_id = pc._id
#               AND pl._deleted IS NULL
#         )                                                   AS brand_count,
#         (
#             SELECT COALESCE(
#                 array_agg(DISTINCT pb.name ORDER BY pb.name),
#                 ARRAY[]::varchar[]
#             )
#             FROM "{SCHEMA}".product_line AS pl
#             JOIN "{SCHEMA}".product_brand AS pb
#                 ON pb._id = pl.brand_id
#                AND pb._deleted IS NULL
#             WHERE pl.category_id = pc._id
#               AND pl._deleted IS NULL
#         )                                                   AS brand_names
#     FROM "{SCHEMA}".product_category AS pc
#     WHERE pc._deleted IS NULL
#     ORDER BY pc.name;
#     """
# )
 
 
# ─────────────────────────────────────────────────────────────────────────────
# VIEW 2 — Brand + product line list (by category)
# Returns: one row per (brand, product_line) pair
# Usage: Level 2 navigation — filter by category_id on the application side
# ─────────────────────────────────────────────────────────────────────────────
# product_brand_line_list_view = PGView(
#     schema=SCHEMA,
#     signature="_product_brand_line_list",
#     definition=f"""
#     SELECT
#         pb._id,                  
#         pb.name,                
#         pb.description,        
#         pb._realm,               
#         pb._created,           
#         pb._updated,           
#         pb._etag,                
#         pl._id                  AS line_id,
#         pl.name                 AS line_name,
#         pl.category_id,
#         pc.name                 AS category_name,
#         pl._created             AS line_created,
#         pl._updated             AS line_updated,
#         pl._etag                AS line_etag,
#         (
#             SELECT COUNT(*)
#             FROM "{SCHEMA}".product AS p
#             WHERE p.line_id = pl._id
#               AND p._deleted IS NULL
#         )                       AS product_count
#     FROM "{SCHEMA}".product_brand AS pb
#     JOIN "{SCHEMA}".product_line AS pl
#         ON pl.brand_id = pb._id
#         AND pl._deleted IS NULL
#     JOIN "{SCHEMA}".product_category AS pc
#         ON pc._id = pl.category_id
#         AND pc._deleted IS NULL
#     WHERE pb._deleted IS NULL
#     ORDER BY pb.name, pl.name;
#     """
# )
category_brand_list_view = PGView(
    schema=SCHEMA,
    signature="_category_brand_list",
    definition=f"""
    SELECT
        pb._id,
        pb._created,
        pb._updated,
        pb._creator,
        pb._updater,
        pb._deleted,
        pb._etag,
        pb._realm,
        pb.name,
        pb.description,
        pb.slug,
        pb.logo_url,
        -- category this brand is associated with (via product → product_category_mapping)
        pc._id                                                      AS category_id,
        pc.name                                                     AS category_name,
        (
            SELECT COUNT(DISTINCT p2._id)
            FROM "{SCHEMA}".product                   AS p2
            JOIN "{SCHEMA}".product_category_mapping  AS pcm2
                ON pcm2.product_id   = p2._id
               AND pcm2.category_id  = pc._id
               AND pcm2._deleted IS NULL
            WHERE p2.brand_id  = pb._id
              AND p2._deleted IS NULL
        )                                                           AS product_count
    FROM "{SCHEMA}".product_brand             AS pb
    -- reach categories through products that belong to this brand
    JOIN "{SCHEMA}".product                   AS p
        ON p.brand_id  = pb._id
       AND p._deleted IS NULL
    JOIN "{SCHEMA}".product_category_mapping  AS pcm
        ON pcm.product_id  = p._id
       AND pcm._deleted IS NULL
    JOIN "{SCHEMA}".product_category          AS pc
        ON pc._id = pcm.category_id
       AND pc._deleted IS NULL
    WHERE pb._deleted IS NULL
    GROUP BY
        pb._id, pb._created, pb._updated, pb._creator, pb._updater,
        pb._deleted, pb._etag, pb._realm, pb.name, pb.description,
        pb.slug, pb.logo_url,
        pc._id, pc.name
    ORDER BY pc.name, pb.name;
    """
)


# ---------------------------------------------------------------------------
# 2. product_line list inside a brand
#    Each row is one product_line; aggregates products that belong to it.
# ---------------------------------------------------------------------------
category_brand_line_list_view = PGView(
    schema=SCHEMA,
    signature="_category_brand_line_list",
    definition=f"""
    SELECT
        pl._id,
        pl._created,
        pl._updated,
        pl._creator,
        pl._updater,
        pl._deleted,
        pl._etag,
        pl._realm,
        pl.name,
        pl.description,
        pl.slug,
        pl.brand_id,
        pb.name                                                     AS brand_name,
        pb.logo_url                                                 AS brand_logo_url,
        (
            SELECT COUNT(*)
            FROM "{SCHEMA}".product AS p
            WHERE p.line_id  = pl._id
              AND p._deleted IS NULL
        )                                                           AS product_count,
        (
            SELECT COALESCE(
                array_agg(DISTINCT pc.name ORDER BY pc.name),
                ARRAY[]::varchar[]
            )
            FROM "{SCHEMA}".product                  AS p
            JOIN "{SCHEMA}".product_category_mapping AS pcm
                ON pcm.product_id  = p._id
               AND pcm._deleted IS NULL
            JOIN "{SCHEMA}".product_category         AS pc
                ON pc._id = pcm.category_id
               AND pc._deleted IS NULL
            WHERE p.line_id  = pl._id
              AND p._deleted IS NULL
        )                                                           AS category_names,
        (
            SELECT pcm.category_id
            FROM "{SCHEMA}".product                  AS p
            JOIN "{SCHEMA}".product_category_mapping AS pcm
                ON pcm.product_id = p._id
               AND pcm._deleted IS NULL
               AND pcm.is_primary = TRUE
            WHERE p.line_id  = pl._id
              AND p._deleted IS NULL
            LIMIT 1
        )                                                         AS category_id
    FROM "{SCHEMA}".product_line  AS pl
    JOIN "{SCHEMA}".product_brand AS pb ON pb._id = pl.brand_id
                                       AND pb._deleted IS NULL
    WHERE pl._deleted IS NULL
    ORDER BY pb.name, pl.name;
    """
)

category_brand_series_list_view = PGView(
    schema=SCHEMA,
    signature="_category_brand_series_list",
    definition=f"""
    SELECT
        ps._id,
        ps._created,
        ps._updated,
        ps._creator,
        ps._updater,
        ps._deleted,
        ps._etag,
        ps._realm,
        ps.name,
        ps.description,
        ps.slug,
        ps.line_id,
        pl.name                                                     AS line_name,
        pl.brand_id,
        pb.name                                                     AS brand_name,
        pb.logo_url                                                 AS brand_logo_url,
        (
            SELECT COUNT(*)
            FROM "{SCHEMA}".product AS p
            WHERE p.series_id = ps._id
              AND p._deleted IS NULL
        )                                                           AS product_count,
        (
            SELECT COALESCE(
                array_agg(DISTINCT pc.name ORDER BY pc.name),
                ARRAY[]::varchar[]
            )
            FROM "{SCHEMA}".product                  AS p
            JOIN "{SCHEMA}".product_category_mapping AS pcm
                ON pcm.product_id  = p._id
               AND pcm._deleted IS NULL
            JOIN "{SCHEMA}".product_category         AS pc
                ON pc._id = pcm.category_id
               AND pc._deleted IS NULL
            WHERE p.series_id = ps._id
              AND p._deleted IS NULL
        )                                                           AS category_names,
        (
            SELECT pcm.category_id
            FROM "{SCHEMA}".product                  AS p
            JOIN "{SCHEMA}".product_category_mapping AS pcm
                ON pcm.product_id = p._id
               AND pcm._deleted IS NULL
               AND pcm.is_primary = TRUE
            WHERE p.series_id = ps._id
              AND p._deleted IS NULL
            LIMIT 1
        )                                                           AS category_id
    FROM "{SCHEMA}".product_series AS ps
    JOIN "{SCHEMA}".product_line   AS pl ON pl._id = ps.line_id
                                        AND pl._deleted IS NULL
    JOIN "{SCHEMA}".product_brand  AS pb ON pb._id = pl.brand_id
                                        AND pb._deleted IS NULL
    WHERE ps._deleted IS NULL
    ORDER BY pb.name, pl.name, ps.name;
    """
)

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
        p.slug,
        p.status,
        -- brand
        p.brand_id,
        pb.name                                                     AS brand_name,
        -- line
        p.line_id,
        pl.name                                                     AS line_name,
        -- series
        p.series_id,
        ps.name                                                     AS series_name,
        -- primary category
        (
            SELECT pcm.category_id
            FROM "{SCHEMA}".product_category_mapping AS pcm
            WHERE pcm.product_id = p._id
              AND pcm.is_primary  = TRUE
              AND pcm._deleted IS NULL
            LIMIT 1
        )                                                           AS category_id,
        (
            SELECT pc.name
            FROM "{SCHEMA}".product_category_mapping AS pcm
            JOIN "{SCHEMA}".product_category          AS pc
                ON pc._id        = pcm.category_id
               AND pc._deleted IS NULL
            WHERE pcm.product_id = p._id
              AND pcm.is_primary  = TRUE
              AND pcm._deleted IS NULL
            LIMIT 1
        )                                                           AS category_name,
        -- primary image
        (
            SELECT pi.image_url
            FROM "{SCHEMA}".product_image AS pi
            WHERE pi.product_id  = p._id
              AND pi.is_primary   = TRUE
              AND pi._deleted IS NULL
            ORDER BY pi.sort_order
            LIMIT 1
        )                                                           AS primary_image_url,
        -- variant fields (from the first active variant ordered by base_price ASC)
        pv.sku,
        pv.price,
        pv.base_price,
        pv.stock_quantity,
        pv.status                                                   AS variant_status,
        pv.tag
    FROM "{SCHEMA}".product          AS p
    LEFT JOIN "{SCHEMA}".product_brand  AS pb ON pb._id    = p.brand_id
                                             AND pb._deleted IS NULL
    LEFT JOIN "{SCHEMA}".product_line   AS pl ON pl._id    = p.line_id
                                             AND pl._deleted IS NULL
    LEFT JOIN "{SCHEMA}".product_series AS ps ON ps._id    = p.series_id
                                             AND ps._deleted IS NULL
    -- pick the single cheapest active variant per product
    LEFT JOIN LATERAL (
        SELECT
            pv2.sku,
            pv2.price,
            pv2.base_price,
            pv2.stock_quantity,
            pv2.status,
            pv2.tag
        FROM "{SCHEMA}".product_variant AS pv2
        WHERE pv2.product_id = p._id
          AND pv2._deleted IS NULL
        ORDER BY pv2.base_price ASC
        LIMIT 1
    ) AS pv ON TRUE
    WHERE p._deleted IS NULL
    ORDER BY p.name;
    """
)

# ---------------------------------------------------------------------------
# 3. product_variant list inside a product
#    One row per variant; includes resolved spec values via product_spec_flat.
# ---------------------------------------------------------------------------
product_variant_list_view = PGView(
    schema=SCHEMA,
    signature="_product_variant_list",
    definition=f"""
    SELECT
        pv._id,
        pv._created,
        pv._updated,
        pv._creator,
        pv._updater,
        pv._deleted,
        pv._etag,
        pv._realm,
        pv.product_id,
        p.name                                                      AS product_name,
        p.slug                                                      AS product_slug,
        p.status                                                    AS product_status,
        pv.sku,
        pv.price,
        pv.base_price,
        pv.stock_quantity,
        pv.status,
        pv.tag,
        pv.attributes,
        -- primary image for this variant (fallback to product primary image)
        COALESCE(
            (
                SELECT pi.image_url
                FROM "{SCHEMA}".product_image AS pi
                WHERE pi.variant_id = pv._id
                  AND pi._deleted IS NULL
                LIMIT 1
            ),
            (
                SELECT pi.image_url
                FROM "{SCHEMA}".product_image AS pi
                WHERE pi.product_id = pv.product_id
                  AND pi.variant_id IS NULL
                  AND pi.is_primary  = TRUE
                  AND pi._deleted IS NULL
                LIMIT 1
            )
        )                                                           AS primary_image_url,
        -- all images for this variant
        (
            SELECT COALESCE(
                array_agg(pi.image_url ORDER BY pi.sort_order),
                ARRAY[]::varchar[]
            )
            FROM "{SCHEMA}".product_image AS pi
            WHERE pi.variant_id = pv._id
              AND pi._deleted IS NULL
        )                                                           AS image_urls,
        -- flat spec JSON blob (pre-computed)
        psf.specs_json                                              AS specs
    FROM "{SCHEMA}".product_variant    AS pv
    JOIN "{SCHEMA}".product            AS p   ON p._id  = pv.product_id
                                             AND p._deleted IS NULL
    LEFT JOIN "{SCHEMA}".product_spec_flat AS psf ON psf.product_id = pv.product_id
                                                 AND psf._id        = pv._id
    WHERE pv._deleted IS NULL
    ORDER BY p.name, pv.sku;
    """
)
# ---------------------------------------------------------------------------
# 4. product_detail view  (single-product detail, all relations denormalised)
#    Intended for a detail page / API endpoint – one row per product.
# ---------------------------------------------------------------------------
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
        p.slug,
        p.status,
        -- brand
        p.brand_id,
        pb.name                                                     AS brand_name,
        pb.slug                                                     AS brand_slug,
        pb.logo_url                                                 AS brand_logo_url,
        -- product line
        p.line_id,
        pl.name                                                     AS line_name,
        pl.slug                                                     AS line_slug,
        -- series (product_series links to product_line via line_id, not directly to product)
        p.series_id,
        ps.name                                                     AS series_name,
        ps.slug                                                     AS series_slug,
        -- primary category
        (
            SELECT pc._id
            FROM "{SCHEMA}".product_category_mapping AS pcm
            JOIN "{SCHEMA}".product_category          AS pc
                ON pc._id        = pcm.category_id
               AND pc._deleted IS NULL
            WHERE pcm.product_id = p._id
              AND pcm.is_primary  = TRUE
              AND pcm._deleted IS NULL
            LIMIT 1
        )                                                           AS category_id,
        (
            SELECT pc.name
            FROM "{SCHEMA}".product_category_mapping AS pcm
            JOIN "{SCHEMA}".product_category          AS pc
                ON pc._id        = pcm.category_id
               AND pc._deleted IS NULL
            WHERE pcm.product_id = p._id
              AND pcm.is_primary  = TRUE
              AND pcm._deleted IS NULL
            LIMIT 1
        )                                                           AS primary_category_name,
        -- all categories
        (
            SELECT COALESCE(
                array_agg(pc.name ORDER BY pc.name),
                ARRAY[]::varchar[]
            )
            FROM "{SCHEMA}".product_category_mapping AS pcm
            JOIN "{SCHEMA}".product_category          AS pc
                ON pc._id        = pcm.category_id
               AND pc._deleted IS NULL
            WHERE pcm.product_id = p._id
              AND pcm._deleted IS NULL
        )                                                           AS category_names,
        -- primary image (product-level, no variant)
        (
            SELECT pi.image_url
            FROM "{SCHEMA}".product_image AS pi
            WHERE pi.product_id  = p._id
              AND pi.is_primary   = TRUE
              AND pi._deleted IS NULL
            LIMIT 1
        )                                                           AS primary_image_url,
        -- all product-level images
        (
            SELECT COALESCE(
                array_agg(pi.image_url ORDER BY pi.sort_order),
                ARRAY[]::varchar[]
            )
            FROM "{SCHEMA}".product_image AS pi
            WHERE pi.product_id = p._id
              AND pi._deleted IS NULL
        )                                                           AS image_urls,
        -- variant summary
        (
            SELECT COUNT(*)
            FROM "{SCHEMA}".product_variant AS pv
            WHERE pv.product_id = p._id
              AND pv._deleted IS NULL
        )                                                           AS variant_count,
        (
            SELECT MIN(pv.price)
            FROM "{SCHEMA}".product_variant AS pv
            WHERE pv.product_id = p._id
              AND pv._deleted IS NULL
        )                                                           AS price_min,
        (
            SELECT MAX(pv.price)
            FROM "{SCHEMA}".product_variant AS pv
            WHERE pv.product_id = p._id
              AND pv._deleted IS NULL
        )                                                           AS price_max,
        (
            SELECT SUM(pv.stock_quantity)
            FROM "{SCHEMA}".product_variant AS pv
            WHERE pv.product_id = p._id
              AND pv._deleted IS NULL
        )                                                           AS total_stock,
        -- flat specs JSON (product_spec_flat PK is composite: product_id + _id where _id is variant)
        -- join on product_id only to get the product-level flat spec row
        psf.specs_json                                              AS specs,
        -- structured spec groups with nested values
        (
            SELECT COALESCE(
                json_agg(
                    json_build_object(
                        'group_id',   psg._id,
                        'group_name', psg.name,
                        'sort_order', psg.sort_order,
                        'values', (
                            SELECT COALESCE(
                                json_agg(
                                    json_build_object(
                                        'key',           psv.key,
                                        'label',         psv.label,
                                        'value_text',    psv.value_text,
                                        'value_number',  psv.value_number,
                                        'value_boolean', psv.value_boolean,
                                        'value_unit',    psv.value_unit,
                                        'is_filterable', psv.is_filterable,
                                        'sort_order',    psv.sort_order
                                    )
                                    ORDER BY psv.sort_order
                                ),
                                '[]'::json
                            )
                            FROM "{SCHEMA}".product_spec_value AS psv
                            WHERE psv.product_spec_group_id = psg._id
                              AND psv._deleted IS NULL
                        )
                    )
                    ORDER BY psg.sort_order
                ),
                '[]'::json
            )
            FROM "{SCHEMA}".product_spec_group AS psg
            WHERE psg.product_id = p._id
              AND psg._deleted IS NULL
        )                                                           AS spec_groups
    FROM "{SCHEMA}".product          AS p
    LEFT JOIN "{SCHEMA}".product_brand  AS pb  ON pb._id    = p.brand_id
                                              AND pb._deleted IS NULL
    LEFT JOIN "{SCHEMA}".product_line   AS pl  ON pl._id    = p.line_id
                                              AND pl._deleted IS NULL
    LEFT JOIN "{SCHEMA}".product_series AS ps  ON ps._id    = p.series_id
                                              AND ps._deleted IS NULL
    LEFT JOIN "{SCHEMA}".product_spec_flat AS psf ON psf.product_id = p._id
    WHERE p._deleted IS NULL
    ORDER BY p.name;
    """
)
# product_detail_view = PGView(
#     schema=SCHEMA,
#     signature="_product_detail",
#     definition=f"""
#     SELECT
#         p._id,
#         p._created,
#         p._updated,
#         p._creator,
#         p._updater,
#         p._deleted,
#         p._etag,
#         p._realm,
#         p.name,
#         p.description,
#         p.slug,
#         p.status,
#         -- brand
#         p.brand_id,
#         pb.name                                                     AS brand_name,
#         pb.slug                                                     AS brand_slug,
#         pb.logo_url                                                 AS brand_logo_url,
#         -- product line
#         p.line_id,
#         pl.name                                                     AS line_name,
#         pl.slug                                                     AS line_slug,
#         -- series
#         p.series_id,
#         ps.name                                                     AS series_name,
#         ps.slug                                                     AS series_slug,
#         -- primary category
#         (
#             SELECT pc._id
#             FROM "{SCHEMA}".product_category_mapping AS pcm
#             JOIN "{SCHEMA}".product_category          AS pc
#                 ON pc._id        = pcm.category_id
#                AND pc._deleted IS NULL
#             WHERE pcm.product_id = p._id
#               AND pcm.is_primary  = TRUE
#               AND pcm._deleted IS NULL
#             LIMIT 1
#         )                                                           AS category_id,
#         (
#             SELECT pc.name
#             FROM "{SCHEMA}".product_category_mapping AS pcm
#             JOIN "{SCHEMA}".product_category          AS pc
#                 ON pc._id        = pcm.category_id
#                AND pc._deleted IS NULL
#             WHERE pcm.product_id = p._id
#               AND pcm.is_primary  = TRUE
#               AND pcm._deleted IS NULL
#             LIMIT 1
#         )                                                           AS primary_category_name,
#         -- all categories
#         (
#             SELECT COALESCE(
#                 array_agg(pc.name ORDER BY pc.name),
#                 ARRAY[]::varchar[]
#             )
#             FROM "{SCHEMA}".product_category_mapping AS pcm
#             JOIN "{SCHEMA}".product_category          AS pc
#                 ON pc._id        = pcm.category_id
#                AND pc._deleted IS NULL
#             WHERE pcm.product_id = p._id
#               AND pcm._deleted IS NULL
#         )                                                           AS category_names,
#         -- primary image
#         (
#             SELECT pi.image_url
#             FROM "{SCHEMA}".product_image AS pi
#             WHERE pi.product_id  = p._id
#               AND pi.is_primary   = TRUE
#               AND pi._deleted IS NULL
#             LIMIT 1
#         )                                                           AS primary_image_url,
#         -- all product-level images
#         (
#             SELECT COALESCE(
#                 array_agg(pi.image_url ORDER BY pi.sort_order),
#                 ARRAY[]::varchar[]
#             )
#             FROM "{SCHEMA}".product_image AS pi
#             WHERE pi.product_id = p._id
#               AND pi._deleted IS NULL
#         )                                                           AS image_urls,
#         -- variant summary
#         (
#             SELECT COUNT(*)
#             FROM "{SCHEMA}".product_variant AS pv
#             WHERE pv.product_id = p._id
#               AND pv._deleted IS NULL
#         )                                                           AS variant_count,
#         (
#             SELECT MIN(pv.price)
#             FROM "{SCHEMA}".product_variant AS pv
#             WHERE pv.product_id = p._id
#               AND pv._deleted IS NULL
#         )                                                           AS price_min,
#         (
#             SELECT MAX(pv.price)
#             FROM "{SCHEMA}".product_variant AS pv
#             WHERE pv.product_id = p._id
#               AND pv._deleted IS NULL
#         )                                                           AS price_max,
#         (
#             SELECT SUM(pv.stock_quantity)
#             FROM "{SCHEMA}".product_variant AS pv
#             WHERE pv.product_id = p._id
#               AND pv._deleted IS NULL
#         )                                                           AS total_stock,
#         -- specs
#         psf.specs_json                                              AS specs,
#         -- structured spec groups
#         (
#             SELECT COALESCE(
#                 json_agg(
#                     json_build_object(
#                         'group_id',   psg._id,
#                         'group_name', psg.name,
#                         'sort_order', psg.sort_order,
#                         'values', (
#                             SELECT COALESCE(
#                                 json_agg(
#                                     json_build_object(
#                                         'key',           psv.key,
#                                         'label',         psv.label,
#                                         'value_text',    psv.value_text,
#                                         'value_number',  psv.value_number,
#                                         'value_boolean', psv.value_boolean,
#                                         'value_unit',    psv.value_unit,
#                                         'is_filterable', psv.is_filterable,
#                                         'sort_order',    psv.sort_order
#                                     )
#                                     ORDER BY psv.sort_order
#                                 ),
#                                 '[]'::json
#                             )
#                             FROM "{SCHEMA}".product_spec_value AS psv
#                             WHERE psv.product_spec_group_id = psg._id
#                               AND psv._deleted IS NULL
#                         )
#                     )
#                     ORDER BY psg.sort_order
#                 ),
#                 '[]'::json
#             )
#             FROM "{SCHEMA}".product_spec_group AS psg
#             WHERE psg.product_id = p._id
#               AND psg._deleted IS NULL
#         )                                                           AS spec_groups,
#         -- review aggregates
#         COALESCE(rv.review_count, 0)                                AS review_count,
#         rv.avg_star
#     FROM "{SCHEMA}".product          AS p
#     LEFT JOIN "{SCHEMA}".product_brand  AS pb  ON pb._id    = p.brand_id
#                                               AND pb._deleted IS NULL
#     LEFT JOIN "{SCHEMA}".product_line   AS pl  ON pl._id    = p.line_id
#                                               AND pl._deleted IS NULL
#     LEFT JOIN "{SCHEMA}".product_series AS ps  ON ps._id    = p.series_id
#                                               AND ps._deleted IS NULL
#     LEFT JOIN "{SCHEMA}".product_spec_flat AS psf ON psf.product_id = p._id
#     LEFT JOIN LATERAL (
#         SELECT
#             COUNT(*)                                                AS review_count,
#             ROUND(AVG(cr.star)::NUMERIC, 2)                        AS avg_star
#         FROM "{SCHEMA}".customer_review AS cr
#         WHERE cr.product_id = p._id
#           AND cr.depth       = 0
#           AND cr.star        IS NOT NULL
#     ) AS rv ON TRUE
#     WHERE p._deleted IS NULL
#     ORDER BY p.name;
#     """
# )
 
 
# # ─────────────────────────────────────────────────────────────────────────────
# # VIEW 3 — Product list (card view)
# # Returns: one row per product with primary image and active sale price
# # Usage: Level 2 product grid — filter by line_id or brand_id
# # ─────────────────────────────────────────────────────────────────────────────
# product_list_view = PGView(
#     schema=SCHEMA,
#     signature="_product_list",
#     definition=f"""
#     SELECT
#         p._id,
#         p._created,
#         p._updated,
#         p._creator,
#         p._updater,
#         p._deleted,
#         p._etag,
#         p._realm,
#         p.name,
#         p.description,
#         p.status,
#         p.line_id,
#         pl.name                                             AS line_name,
#         pl.brand_id                                         AS brand_id,
#         pb.name                                             AS brand_name,
#         pl.category_id                                      AS category_id,
#         pc.name                                             AS category_name,
#         p.base_price,
#         pv.price,
#         pv.sku,
#         pv.stock_quantity,
#         CASE
#             WHEN pr.discount_percent IS NOT NULL
#             THEN ROUND(p.base_price * (1.0 - pr.discount_percent / 100.0), 0)
#             ELSE p.base_price
#         END                                                 AS sale_price,
#         pr.discount_percent,
#         pr.gift,
#         pr.valid_from                                       AS promo_valid_from,
#         pr.valid_to                                         AS promo_valid_to,
#         pi.image_url                                        AS primary_image_url
#     FROM "{SCHEMA}".product AS p
#     JOIN "{SCHEMA}".product_line AS pl
#         ON pl._id = p.line_id
#         AND pl._deleted IS NULL
#     JOIN "{SCHEMA}".product_brand AS pb
#         ON pb._id = pl.brand_id
#         AND pb._deleted IS NULL
#     JOIN "{SCHEMA}".product_category AS pc
#         ON pc._id = pl.category_id
#         AND pc._deleted IS NULL
#     LEFT JOIN "{SCHEMA}".product_variant AS pv
#         ON pv.product_id = p._id
#         AND pv._deleted IS NULL
#     LEFT JOIN "{SCHEMA}".product_image AS pi
#         ON pi.product_id = p._id
#         AND pi.is_primary = TRUE
#         AND pi._deleted IS NULL
#     LEFT JOIN "{SCHEMA}".promotion AS pr
#         ON pr.product_id = p._id
#         AND NOW() BETWEEN pr.valid_from AND pr.valid_to
#         AND pr._deleted IS NULL
#     WHERE p._deleted IS NULL;
#     """
# )
 
 
# ─────────────────────────────────────────────────────────────────────────────
# VIEW 4 — Product detail (full info + all images + variants)
# Returns: one row per product variant with all product metadata and images
# Usage: Level 3 product detail page
# ─────────────────────────────────────────────────────────────────────────────
# product_detail_view = PGView(
#     schema=SCHEMA,
#     signature="_product_detail",
#     definition=f"""
#     SELECT
#         p._id,                                               
#         p._created,
#         p._updated,
#         p._creator,
#         p._updater,
#         p._deleted,
#         p._etag,
#         p._realm,
#         p.name,
#         p.description,
#         p.status,
#         p.llm_spec_text,
#         p.line_id,
#         pl.name                                             AS line_name,
#         pl.brand_id,
#         pb.name                                             AS brand_name,
#         pb.description                                      AS brand_description,
#         pl.category_id,
#         pc.name                                             AS category_name,
#         pv._id                                              AS variant_id,
#         pv.sku,
#         p.base_price,
#         pv.price,
#         pv.stock_quantity,
#         pv.attributes                                       AS variant_attributes,
#         CASE
#             WHEN pr.discount_percent IS NOT NULL
#             THEN ROUND(p.base_price * (1.0 - pr.discount_percent / 100.0), 0)
#             ELSE p.base_price
#         END                                                 AS sale_price,
#         pr.discount_percent,
#         pr.gift,
#         pr.valid_from                                       AS promo_valid_from,
#         pr.valid_to                                         AS promo_valid_to,
#         COALESCE(img.images, ARRAY[]::json[])               AS images,
#         psf.specs_json
#     FROM "{SCHEMA}".product AS p
#     JOIN "{SCHEMA}".product_line AS pl
#         ON pl._id = p.line_id
#         AND pl._deleted IS NULL
#     JOIN "{SCHEMA}".product_brand AS pb
#         ON pb._id = pl.brand_id
#         AND pb._deleted IS NULL
#     JOIN "{SCHEMA}".product_category AS pc
#         ON pc._id = pl.category_id
#         AND pc._deleted IS NULL
#     LEFT JOIN "{SCHEMA}".product_variant AS pv
#         ON pv.product_id = p._id
#         AND pv._deleted IS NULL
#     LEFT JOIN "{SCHEMA}".promotion AS pr
#         ON pr.product_id = p._id
#         AND NOW() BETWEEN pr.valid_from AND pr.valid_to
#         AND pr._deleted IS NULL
#     LEFT JOIN (
#         SELECT
#             product_id,
#             array_agg(
#                 json_build_object(
#                     'image_url',  image_url,
#                     'is_primary', is_primary
#                 ) ORDER BY is_primary DESC, _created ASC
#             ) AS images
#         FROM "{SCHEMA}".product_image
#         WHERE _deleted IS NULL
#         GROUP BY product_id
#     ) AS img
#         ON img.product_id = p._id
#     LEFT JOIN "{SCHEMA}".product_spec_flat AS psf
#         ON psf.product_id = p._id
#         AND psf._deleted IS NULL
#     WHERE p._deleted IS NULL;
#     """
# )
 
 
# ─────────────────────────────────────────────────────────────────────────────
# VIEW 5 — Product specification (grouped)
# Returns: one row per spec attribute value, ordered by group/attr sort_order
# Usage: Level 3 spec table — filter by product_id
# ─────────────────────────────────────────────────────────────────────────────
# product_spec_detail_view = PGView(
#     schema=SCHEMA,
#     signature="_product_spec_detail",
#     definition=f"""
#     SELECT
#         psv._id,                 
#         psv._created,
#         psv._updated,
#         psv._etag,
#         psv._realm,
#         psv.product_id,
#         p.name                  AS product_name,
#         sg._id                  AS group_id,
#         sg.name                 AS group_name,
#         sg.sort_order           AS group_sort_order,
#         sg.category_id,
#         sa._id                  AS attribute_id,
#         sa.name                 AS attribute_name,
#         sa.data_type,
#         sa.unit,
#         sa.sort_order           AS attribute_sort_order,
#         psv.value_text,
#         psv.value_number,
#         psv.value_boolean,
#         psv.value_json,
#         CASE sa.data_type::text
#             WHEN 'TEXT'        THEN psv.value_text
#             WHEN 'NUMBER'      THEN CONCAT(psv.value_number::text, ' ', sa.unit)
#             WHEN 'BOOLEAN'     THEN CASE WHEN psv.value_boolean THEN 'Có' ELSE 'Không' END
#             WHEN 'JSON'        THEN psv.value_json::text
#             WHEN 'SELECT'      THEN psv.value_text
#             WHEN 'MULTISELECT' THEN psv.value_text
#             ELSE NULL
#         END                     AS display_value 
#     FROM "{SCHEMA}".product_spec_value AS psv
#     JOIN "{SCHEMA}".product AS p
#         ON p._id = psv.product_id
#         AND p._deleted IS NULL
#     JOIN "{SCHEMA}".spec_attribute AS sa
#         ON sa._id = psv.attribute_id
#         AND sa._deleted IS NULL
#     JOIN "{SCHEMA}".spec_group AS sg
#         ON sg._id = sa.group_id
#         AND sg._deleted IS NULL
#     WHERE psv._deleted IS NULL
#     ORDER BY sg.sort_order, sa.sort_order;
#     """
# )
 



def register_pg_entities(allow_flag):
    if not allow_flag:
        logger.info('REGISTER_PG_ENTITIES is disabled or not set.')
        return
    logger.info('Registering PG entities for ecom_product')
    register_entities([
        category_brand_list_view,
        category_brand_line_list_view,
        category_brand_series_list_view,
        product_list_view,
        product_variant_list_view,
        product_detail_view
        # product_category_list_view,
        # product_brand_line_list_view,
        # product_list_view,
        # product_detail_view,
        # product_spec_detail_view,
        # product_review_list_view,
    ])


register_pg_entities(os.environ.get('REGISTER_PG_ENTITIES'))