from openai import OpenAI

from src.config.settings import llm_model
from src.services.llm.llm_client import LLMClient


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, history: list[dict]) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=history,
            model=llm_model,
        )
        return chat_completion.choices[0].message.content
