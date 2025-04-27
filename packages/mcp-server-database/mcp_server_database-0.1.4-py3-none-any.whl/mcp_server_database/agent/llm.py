from openai import AsyncOpenAI

from dotenv import load_dotenv
import os
load_dotenv(verbose=True)


class LLM:
    """创建LLM模型"""
    def __init__(self, temperature: float = 0.0, max_tokens: int = 8190, system_prompt: str = None) -> None:
        self.model = os.getenv('model')
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt

    @property
    def client(self):
        """用到时才初始化 OpenAI 客户端"""
        api_key = os.getenv("api_key")
        base_url = os.getenv("base_url")
        if not api_key or not base_url:
            raise ValueError("请配置模型调用信息 OpenAI API")
        return AsyncOpenAI(
                api_key=api_key,
                base_url=base_url
            )

    async def ask(self, query: str) -> str:
        """创建LLM模型"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content
