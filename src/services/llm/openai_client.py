from openai import OpenAI

from src.services.llm.llm_client import LLMClient


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str):
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment or .env")
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, history: list[dict], model: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=history,
            model=model,
        )
        return chat_completion.choices[0].message.content
