from groq import Groq

from src.exceptions import MissingProviderAPIKeyError
from src.services.llm.llm_client import LLMClient


class GroqClient(LLMClient):
    def __init__(self, api_key: str):
        if not api_key:
            raise MissingProviderAPIKeyError("Groq")
        self.client = Groq(api_key=api_key)

    def generate_response(self, history: list[dict], model: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=history,
            model=model,
        )
        return chat_completion.choices[0].message.content
