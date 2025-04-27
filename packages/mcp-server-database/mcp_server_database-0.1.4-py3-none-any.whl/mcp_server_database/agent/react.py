from abc import ABC, abstractmethod
from typing import Optional, List

from sqlalchemy import inspect
from mcp_server_database.agent.base import BaseAgent
from pydantic import Field

from mcp_server_database.agent.engine import CreateEngine
from mcp_server_database.agent.llm import LLM
from mcp_server_database.agent.prompt import THINK_PROMPT, PLAIN_PROMPT, EXECUTE_PROMPT
from mcp_server_database.agent.schema import AgentState
from mcp_server_database.utils import (
    extract_tables_info,
    extract_json,
    get_multi_table_info,
    get_single_table_info,
)


class ReActAgent(CreateEngine):
    name: str = "NLtoSql"

    llm: Optional[LLM] = Field(default_factory=LLM)
    max_steps: int = 1
    current_step: int = 0
    user_prompt: str = Field(None, description="用户问题")
    next_step_prompt: str = Field(None, description="下一步提示指示")

    use_tables: List[str] = Field(default=[], description="用户问题涉及使用的表")
    thought: str = Field(None, description="用户行为分析")
    tables_construction_thought: str = Field(None, description="表结构分析")
    sql: str = Field(None, description="生成的SQL语句")

    async def think(self) -> bool:
        """思考"""
        tables_info = extract_tables_info(self.inspector)
        think_prompt = THINK_PROMPT.format(
            tables_info=tables_info, query_str=self.user_prompt
        )
        response = await self.llm.ask(think_prompt)
        result = extract_json(response)
        print("思考：", result)
        self.use_tables = result["tables"].split(",")
        self.thought = result["thought"]
        return True

    async def plan(self) -> bool:
        """计划"""
        tables_info = [
            get_single_table_info(self.inspector, table) for table in self.use_tables
        ]
        tables_info_str = "\n\n".join(tables_info)
        plan_prompt = PLAIN_PROMPT.format(
            tables_info_str=tables_info_str,
            query_str=self.user_prompt,
            dialect=self.database,
        )
        response = await self.llm.ask(plan_prompt)
        result = extract_json(response)
        print("计划：", result)
        self.tables_construction_thought = result["table_thought"]
        self.sql = result["sql"]
        return True

    async def act(self) -> str:
        """执行"""
        if self.sql:
            sql_type = self.sql.strip().split()[0].upper()
            if sql_type in [
                "SELECT",
                "SHOW",
                "WITH",
                "EXPLAIN",
                "DESCRIBE",
                "DESC",
                "USE",
                "CHECK",
                "FETCH",
            ]:
                result = self.run(self.sql)
            else:
                result = "涉及非查询操作，请手动执行！"
            return EXECUTE_PROMPT.format(
                query_str=self.user_prompt,
                thought=self.thought,
                table_thought=self.tables_construction_thought,
                sql=self.sql,
                result=result,
            )
        else:
            return "未生成对应的sql语句，请重新输入对应数据库内有关的内容，我将为您解答"

    async def step(self) -> str:
        """执行步骤"""
        await self.think()
        await self.plan()
        return await self.act()

    @classmethod
    async def create(cls, **kwargs):
        """初始化 ReActAgent（包括数据库引擎和 LLM）"""
        instance = await super().create(**kwargs)  # 调用 CreateEngine.create()
        # instance.llm = LLM(system_prompt=instance.system_prompt)  # 显式初始化 LLM
        return instance

    async def cleanup(self):
        """重置初始步骤"""
        for field in [
            "llm",
            "user_prompt",
            "thought",
            "sql",
            "tables_construction_thought",
            "next_step_prompt",
        ]:
            setattr(self, field, None)
        self.use_tables = []
        self.current_step = 0

    async def query(self, request: Optional[str] = None) -> str:
        try:
            return await super().query(request)
        finally:
            await self.cleanup()
