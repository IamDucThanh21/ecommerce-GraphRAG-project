import logging
from typing import Optional
import google.generativeai as genai
from .config import get_gemini_api_key, get_gemini_model

logger = logging.getLogger(__name__)


class AIClient:
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or get_gemini_api_key()
        self.model_name = model_name or get_gemini_model()

        if not self.api_key:
            logger.warning("No Gemini API key found; AI calls will likely fail.")

        try:
            genai.configure(api_key=self.api_key)
            self._model = genai.GenerativeModel(self.model_name)
        except Exception as exc:
            logger.exception("Failed to configure Gemini client: %s", exc)
            self._model = None

    def generate_content(self, prompt: str) -> str:
        if not self._model:
            raise RuntimeError("Gemini model not configured")
        try:
            response = self._model.generate_content(prompt)
            # text = getattr(response, "text", None)
            # if text is None:
            #     text = str(response)
            # return text.strip()
            return response.text.strip()
        except Exception:
            logger.exception("AI generation failed")
            raise

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        prompt = f"{system_prompt}\n\n{user_prompt}"
        return self.generate_content(prompt)


def init_client(api_key: Optional[str] = None, model_name: Optional[str] = None) -> "AIClient":
    return AIClient(api_key=api_key, model_name=model_name)