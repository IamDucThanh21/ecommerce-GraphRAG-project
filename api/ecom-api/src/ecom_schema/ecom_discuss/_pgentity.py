import os
from ecom_schema._meta import logger
from . import SCHEMA


from alembic_utils.pg_view import PGView
from alembic_utils.replaceable_entity import register_entities


comment_detail_view = PGView(
    schema=SCHEMA,
    signature="_comment_detail",
    definition=f"""
    SELECT
        c._id,
        c._created,
        c._updated,
        c._creator,
        c._updater,
        c._deleted,
        c._etag,
        c._realm,
        c.resource_type,
        c.resource_id,
        c.user_id,
        c.name_user,
        c.parent_id,
        c.depth,
        c.content,
        c.star,
        -- reply count (admin replies, depth=1, attached to this comment)
        (
            SELECT COUNT(*)
            FROM "{SCHEMA}".comment AS r
            WHERE r.parent_id = c._id
              AND r._deleted IS NULL
        )                                                           AS reply_count,
        -- reaction summary: total count
        (
            SELECT COUNT(*)
            FROM "{SCHEMA}".comment_reaction AS cr
            WHERE cr.comment_id = c._id
              AND cr._deleted IS NULL
        )                                                           AS reaction_count,
        -- reaction summary: breakdown by type as JSON, e.g. {{"like": 3, "love": 1}}
        (
            SELECT COALESCE(
                json_object_agg(reaction_type, reaction_total),
                '{{}}'::json
            )
            FROM (
                SELECT cr.reaction_type, COUNT(*) AS reaction_total
                FROM "{SCHEMA}".comment_reaction AS cr
                WHERE cr.comment_id = c._id
                  AND cr._deleted IS NULL
                GROUP BY cr.reaction_type
            ) AS reaction_breakdown
        )                                                           AS reaction_summary,
        -- selected tags: array of {{option_id, option_name, group_id, group_name}}
        (
            SELECT COALESCE(
                json_agg(
                    json_build_object(
                        'option_id',   rto._id,
                        'option_name', rto.name,
                        'group_id',    rtg._id,
                        'group_name',  rtg.name
                    )
                    ORDER BY rtg.sort_order, rto.sort_order
                ),
                '[]'::json
            )
            FROM "{SCHEMA}".customer_review_tag AS crt
            JOIN "{SCHEMA}".review_tag_option   AS rto
                ON rto._id = crt.option_id
               AND rto._deleted IS NULL
            JOIN "{SCHEMA}".review_tag_group    AS rtg
                ON rtg._id = rto.group_id
               AND rtg._deleted IS NULL
            WHERE crt.review_id = c._id
              AND crt._deleted IS NULL
        )                                                           AS tags
    FROM "{SCHEMA}".comment AS c
    WHERE c._deleted IS NULL
    ORDER BY c._created DESC;
    """
)

review_tag_option_list_view = PGView(
    schema=SCHEMA,
    signature="_review_tag_option_list",
    definition=f"""
    SELECT
        rto._id,
        rto._created,
        rto._updated,
        rto._creator,
        rto._updater,
        rto._deleted,
        rto._etag,
        rto._realm,
        rto.group_id,
        rto.name                                                    AS option_name,
        rto.sort_order                                              AS option_sort_order,
        rtg.name                                                    AS group_name,
        rtg.sort_order                                              AS group_sort_order,
        rtg.category_id
    FROM "{SCHEMA}".review_tag_option AS rto
    JOIN "{SCHEMA}".review_tag_group  AS rtg
        ON rtg._id = rto.group_id
       AND rtg._deleted IS NULL
    WHERE rto._deleted IS NULL
    ORDER BY rtg.sort_order, rtg.name, rto.sort_order, rto.name;
    """
)

comment_summary_view = PGView(
    schema=SCHEMA,
    signature="_comment_summary",
    definition=f"""
    SELECT
        c.resource_id                                               AS _id,
        c.resource_type,
        COUNT(*)                                                    AS num_comments,
        ROUND(AVG(c.star)::NUMERIC, 2)                             AS average_star,
        COALESCE(
            (
                SELECT json_agg(
                    json_build_object(
                        '_id',        rtg._id,
                        'group_name', rtg.name,
                        'num_vote',   (
                            SELECT COUNT(DISTINCT crt.review_id)
                            FROM "{SCHEMA}".customer_review_tag AS crt
                            JOIN "{SCHEMA}".review_tag_option   AS rto
                                ON rto._id      = crt.option_id
                               AND rto.group_id = rtg._id
                               AND rto._deleted IS NULL
                            WHERE crt.review_id IN (
                                SELECT c2._id
                                FROM "{SCHEMA}".comment AS c2
                                WHERE c2.resource_id   = c.resource_id
                                  AND c2.resource_type = c.resource_type
                                  AND c2.depth         = 0
                                  AND c2._deleted      IS NULL
                            )
                            AND crt._deleted IS NULL
                        ),
                        'average', (
                            SELECT ROUND(
                                COALESCE(
                                    SUM(rto.sort_order)::NUMERIC / NULLIF(
                                        COUNT(DISTINCT crt.review_id), 0
                                    ),
                                    0
                                ), 2
                            )
                            FROM "{SCHEMA}".comment AS c2
                            LEFT JOIN "{SCHEMA}".customer_review_tag AS crt
                                ON crt.review_id = c2._id
                            AND crt._deleted  IS NULL
                            LEFT JOIN "{SCHEMA}".review_tag_option   AS rto
                                ON rto._id       = crt.option_id
                            AND rto.group_id  = rtg._id
                            AND rto._deleted  IS NULL
                            WHERE c2.resource_id   = c.resource_id
                            AND c2.resource_type = c.resource_type
                            AND c2.depth         = 0
                            AND c2._deleted      IS NULL
                        )
                    )
                    ORDER BY rtg.sort_order
                )
                FROM "{SCHEMA}".review_tag_group AS rtg
                WHERE rtg._deleted IS NULL
                AND rtg.category_id = (
                    SELECT pcm.category_id
                    FROM "ecom_product".product_category_mapping AS pcm
                    WHERE pcm.product_id = c.resource_id
                        AND pcm.is_primary = TRUE
                        AND pcm._deleted   IS NULL
                    LIMIT 1
                )
            ),
            '[]'::json
        )                                                           AS groups
    FROM "{SCHEMA}".comment AS c
    WHERE c.resource_type = 'PRODUCT'
      AND c.depth         = 0
      AND c._deleted      IS NULL
    GROUP BY c.resource_id, c.resource_type;
    """
)

def register_pg_entities(allow_flag):
    if not allow_flag:
        logger.info('REGISTER_PG_ENTITIES is disabled or not set.')
        return
    logger.info('Registering PG entities for ecom_product')
    register_entities([
        comment_detail_view,
        review_tag_option_list_view,
        comment_summary_view
    ])


register_pg_entities(os.environ.get('REGISTER_PG_ENTITIES'))