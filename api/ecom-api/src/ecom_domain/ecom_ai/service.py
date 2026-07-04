import json
import logging
from typing import Any, Dict, List, Optional
import re
import uuid

from .ai_client import AIClient
from .cypher_gen import generate_cypher
from .neo4j_client import run_query
from .startup import get_driver, get_ai_client

logger = logging.getLogger(__name__)

RESPONSE_SYSTEM_PROMPT = (
    "You are a smartphone recommendation assistant. "
    "Answer in Vietnamese. Be concise. "
    "For each product mention: name, approximate price, and a short reason."
)

def natural_response(
    user_query: str,
    query_result: list[dict],
    context: dict | None = None,
    action: str = "query",
    ai_client: Optional[AIClient] = None,
) -> str:

    context_block = (
        f"\nConversation context:\n{json.dumps(context, ensure_ascii=False, indent=2)}"
        if context else ""
    )

    if action == "compare":
        if len(query_result) == 0:
            return "Không tìm thấy sản phẩm nào trong hệ thống. Vui lòng kiểm tra lại tên sản phẩm."
        elif len(query_result) == 1:
            found = query_result[0]['product_name']
            targets = context.get('other_filters', {}).get('compare_targets', [])
            return f"Chỉ tìm thấy **{found}** trong hệ thống. Sản phẩm còn lại chưa có dữ liệu để so sánh."
        elif len(query_result) == 2:
            p1, p2 = query_result[0], query_result[1]

            prompt = f"""
                Bạn là trợ lý tư vấn điện thoại. Hãy so sánh 2 sản phẩm dưới đây.

                Câu hỏi người dùng:
                {user_query}
                {context_block}

                Dữ liệu sản phẩm (JSON):
                {json.dumps(query_result, ensure_ascii=False, indent=2)}

                Yêu cầu output — viết bằng tiếng Việt, gồm 3 phần:

                1. BẢNG SO SÁNH THÔNG SỐ
                Tạo bảng markdown với các nhóm sau (mỗi nhóm là một section):
                - Màn hình (display_size, display_technology, refresh_rate, brightness_nits, resolution, glass_protection)
                - Camera sau (camera_count, main_camera_mp, main_aperture, ois, optical_zoom, video_recording)
                - Camera trước (selfie_mp, selfie_aperture, selfie_video)
                - Chip & Hiệu năng (chip_name, chip_tier, antutu_score, gpu, cooling)
                - RAM & Bộ nhớ (ram, storage, expandable_storage + liệt kê các phiên bản variant kèm giá)
                - Pin & Sạc (battery_mah, wired_charging, wireless_charging, battery_life_hours, charging_time_min)
                - Thiết kế & Vật liệu (ip_rating, back_material, frame_material, thickness, weight)
                - AI (ai_features_raw, ai_score)
                - Camera quality scores (photo_day, photo_night, video, selfie, avg — scale 1-5)
                Format mỗi section:
                | Thông số | {p1['product_name']} | {p2['product_name']} |
                Đánh dấu ô tốt hơn bằng ✓, điểm tuyệt đối (=5) bằng ⭐

                2. ĐỐI TƯỢNG & MỤC ĐÍCH PHÙ HỢP
                Chỉ liệt kê score >= 3. Đánh dấu score = 5 bằng ⭐.
                Format:
                | Tiêu chí | {p1['product_name']} | {p2['product_name']} |

                3. NHẬN XÉT TỔNG QUAN
                - 3-4 câu highlight điểm mạnh nổi bật của mỗi máy
                - 1-2 câu gợi ý nên chọn máy nào cho nhu cầu gì
                Ngắn gọn, tự nhiên, không liệt kê lại specs.
            """   
    else:
        prompt = f"""
            You are a smartphone recommendation assistant.

            User question:
            {user_query}
            {context_block}

            Database result:
            {json.dumps(query_result, ensure_ascii=False, indent=2)}

            Write a concise Vietnamese response.
            Mention: product name, approximate price, short explanation.
            Be natural and easy to understand.
        """

    return ai_client.generate_content(prompt=prompt)

# def _extract_product_ids(results: List[Dict[str, Any]]) -> List[str]:
#     """Pull unique, ordered product_id values out of the Neo4j result rows.

#     cypher_gen enforces that every row includes `product_id` — this collects
#     them (preserving rank order, de-duplicated) for later persistence into
#     recommendation_item rows.
#     """
#     seen = set()
#     product_ids: List[str] = []
#     for row in results:
#         pid = row.get("product_id")
#         if pid is None:
#             continue
#         pid = str(pid)
#         if pid not in seen:
#             seen.add(pid)
#             product_ids.append(pid)
#     return product_ids

def _extract_product_ids(results: list[dict]) -> list[str]:
    """Pull unique, ordered product_id values out of the Neo4j result rows.
    Handles raw UUID objects, tuples containing UUIDs, and string representations.
    """
    seen = set()
    product_ids: list[str] = []

    for row in results:
        pid = row.get("product_id")
        if pid is None:
            continue

        # Case 1: already a uuid.UUID object
        if isinstance(pid, uuid.UUID):
            pid_str = str(pid)

        # Case 2: tuple containing a UUID, e.g. (UUID('...'),)
        elif isinstance(pid, tuple):
            inner = pid[0]
            pid_str = str(inner) if isinstance(inner, uuid.UUID) else str(inner)

        # Case 3: string representation like "(UUID('edc712ff-...'),)"
        elif isinstance(pid, str):
            match = re.search(
                r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                pid,
                re.IGNORECASE,
            )
            pid_str = match.group(0) if match else pid

        else:
            pid_str = str(pid)

        if pid_str not in seen:
            seen.add(pid_str)
            product_ids.append(pid_str)

    return product_ids


def ask_graph(
    user_query: str,
    driver=None,
    ai_client: Optional[AIClient] = None,
    prior_context: dict | None = None,
) -> Dict[str, Any]:
    """Orchestrate the full pipeline:
    user query -> Cypher -> Neo4j -> natural Vietnamese response.

    Returns:
        {
            "answer": str,            # Vietnamese natural language reply
            "cypher": str,            # generated Cypher query
            "raw_result": list[dict], # raw rows from Neo4j (incl. product_id, product_name, ...)
            "product_ids": list[str], # ordered, de-duplicated product_id list for recommendation_item rows
            "conversation_id": ...,
        }
    """
    ai_client = ai_client or get_ai_client()
    driver = driver or get_driver()

    # Step 1: generate Cypher from user query
    llm_out = generate_cypher(user_query=user_query, prior_context=prior_context, ai_client=ai_client)
    logger.debug("Generated Cypher:\n%s", llm_out)

    action    = llm_out["action"]
    context   = llm_out["context"]
    cypher    = llm_out.get("cypher")
    clarify_q = llm_out.get("clarify_question")
    
    # print()
    # print("=" * 60)
    # print("EXTRACTED CONTEXT")
    # print("=" * 60)
    context = json.dumps(context, ensure_ascii=False, indent=2)
    # print(context)

    print()
    print("=" * 60)
    print(f"ACTION: {action.upper()}")
    print("=" * 60)

    if action == "clarify":
        print(clarify_q)
        return {
            "action":  "clarify",
            "context": context,
            "cypher":  None,
            "raw_result":  None,
            "answer":  clarify_q,
        }
    
    # print(cypher)

    # Step 2: run against Neo4j
    try:
        result = run_query(driver = driver, query = cypher)
    except Exception as exc:
        logger.exception("Cypher execution failed: %s", exc)
        result = []

    # Step 2b: extract product_id list for recommendation persistence
    product_ids = _extract_product_ids(result)
    # print()
    # print("=" * 60)
    # print("RAW RESULT")
    # print("=" * 60)
    # print(result)

    # print()
    # print("=" * 60)
    # print("RAW RESULT")
    # print("=" * 60)
    # print(product_ids)

    # Step 3: parse Neo4j result -> natural language via Gemini
    answer = natural_response(user_query=user_query, 
                              query_result=result, 
                              context=context, 
                              action=action, 
                              ai_client=ai_client)
    
    print(answer)

    # user_prompt = (
    #     f"User question:\n{user_query}\n\n"
    #     f"Database result:\n{json.dumps(results, ensure_ascii=False, indent=2)}"
    # )

    # try:
    #     ai_text = ai_client.chat(
    #         system_prompt=RESPONSE_SYSTEM_PROMPT,
    #         user_prompt=user_prompt,
    #     )
    # except Exception:
    #     logger.exception("AI response generation failed")
    #     ai_text = "Xin lỗi, tôi không thể trả lời ngay bây giờ."

    return {
        "action":  action,
        "context": context,
        "cypher":  cypher,
        "raw_result": result,
        "product_ids": product_ids,
        "answer":  answer,
    }

    return {
        "answer": ai_text,
        "cypher": cypher,
        "raw_result": results,
        "product_ids": product_ids,
        # "conversation_id": conv_id,
    }

# nếu đoạn chat đã tồn tại thì dựa vào đoạn chat cũ chứ không chào lại
# nếu như là