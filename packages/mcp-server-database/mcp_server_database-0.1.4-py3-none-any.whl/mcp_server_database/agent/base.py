from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel, Field, model_validator

from mcp_server_database.agent.llm import LLM
from mcp_server_database.agent.prompt import SYSTEM_PROMPT
from mcp_server_database.agent.schema import AgentState


class BaseAgent(BaseModel, ABC):
    name: str = Field(..., description="智能体名称")
    description: Optional[str] = Field(None, description="作用描述")

    system_prompt: Optional[str] = Field(SYSTEM_PROMPT, description="系统提示词")
    user_prompt: Optional[str] = Field(None, description="用户问题")
    max_steps: int = Field(default=1, description="最大执行步骤数")
    current_step: int = Field(default=0, description="当前执行步骤")
    llm: LLM = None

    class Config:
        # 允许字段使用自定义类型（比如某些非标准类型对象）。
        arbitrary_types_allowed = True
        # 当模型实例化时，允许额外的字段。
        extra = "allow"

    @model_validator(mode="after")
    def initialize_agent(self) -> "BaseAgent":
        if not self.llm.system_prompt:
            self.llm = LLM(system_prompt=self.system_prompt)
        return self

    @abstractmethod
    async def step(self) -> str:
        """执行步骤"""

    async def query(self, query: str) -> str:
        """执行查询"""
        self.user_prompt = query
        while self.current_step < self.max_steps:
            try:
                result = await self.step()
                self.current_step += 1
                return result
            except Exception as e:
                print(f"执行步骤时出错: {e}")
                return "抱歉，我无法执行您的请求。"
