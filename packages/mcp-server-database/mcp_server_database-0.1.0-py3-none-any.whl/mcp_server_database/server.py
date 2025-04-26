import json
from typing import List

from sqlalchemy import create_engine, inspect
from mcp.server.fastmcp import FastMCP
from llama_index.core import SQLDatabase
from llama_index.core.indices.struct_store.sql_retriever import SQLRetriever
from pydantic import BaseModel
from openai import AsyncOpenAI
from prompt import PLAIN_PROMPT, THINK_PROMPT, EXECUTE_PROMPT
from dotenv import load_dotenv
import os

from utils import extract_json, extract_table_info

load_dotenv(verbose=True)

mcp = FastMCP("database")
USER_AGENT = "database/1.0"

def get_engine():
    """创建数据库连接引擎"""
    database = os.getenv("database")
    host = os.getenv("host")
    port = os.getenv("port")
    user = os.getenv("user")
    password = os.getenv("password")
    dbname = os.getenv("dbname")
    return create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8mb4")

async def llm(prompt: str):
    """创建LLM模型"""
    client = AsyncOpenAI(
        api_key=os.getenv("api_key"),
        base_url=os.getenv("base_url")
    )
    response = await client.chat.completions.create(
        model= os.getenv("model"),
        messages=[
            {"role": "system", "content": "你是一个智能数据库助手，你可以帮助用户查询数据库中的内容。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=8190,
    )
    return response

async def think_agent(query: str, sql_database: SQLDatabase) -> List[str]:
    """执行思考"""
    # 获取数据库表名称
    tables = sql_database.get_usable_table_names()
    # 获取对应表信息
    tables_info = [sql_database.get_single_table_info(table) for table in tables]
    # 获取表关键信息
    extract_tables = extract_table_info(tables_info)
    think = THINK_PROMPT.format(tables_info=json.dumps(extract_tables), query_str=query)
    response = await llm(think)
    content = response.choices[0].message.content
    result = extract_json(content)
    print("思考：", result)
    tables = result["tables"].split(",")
    thought = result["thought"]
    return thought, tables

async def plan_agent(query: str, sql_database: SQLDatabase, tables: List[str]):
    """开始计划"""
    tables_info = [sql_database.get_single_table_info(table) for table in tables]
    tables_info_str = "\n\n".join(tables_info)
    plan = PLAIN_PROMPT.format(tables_info_str=tables_info_str, query_str=query, dialect=os.environ.get("database"))
    response = await llm(plan)
    content = response.choices[0].message.content
    result = extract_json(content)
    print("计划：", result)
    return result['table_thought'], result['sql']

async def execute_agent(query: str, sql_retriever: SQLRetriever, sql: str, thought: str, table_thought: str):
    """执行SQL"""
    if sql:
        sql_type = sql.strip().split()[0].upper()
        if sql_type in ['SELECT', 'SHOW', 'WITH', 'EXPLAIN', 'DESCRIBE', 'DESC', 'USE', 'CHECK', 'FETCH']:
            # 执行查询语句
            nodes = sql_retriever.retrieve(sql)
            retrieverd_node = json.dumps(nodes[0].metadata['result'], ensure_ascii=False)
        else:
            retrieverd_node = "涉及非查询操作，请手动执行！"
        result = EXECUTE_PROMPT.format(query_str=query, thought=thought, table_thought=table_thought, sql=sql, result=retrieverd_node)
        print("执行：", result)
        return result
    else:
        return "未查询到对应的信息，请重新输入对应数据库内有关的内容，我将为您解答"


@mcp.tool()
async def nltosql_agent(query: str):
    """
    当用户明确需要查询数据库时，使用该工具。
    该函数将用户问题经过思考、计划和执行三个步骤，最终以markdown格式返回结果。
    输入参数query：用户数据库问题，类型为字符串。
    """
    engine = get_engine()
    sql_database = SQLDatabase(engine)
    sql_retriever = SQLRetriever(sql_database)
    thought, tables = await think_agent(query, sql_database)
    table_thought, sql = await plan_agent(query, sql_database, tables)
    result = await execute_agent(query, sql_retriever, sql, thought, table_thought)
    return result

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
    # import asyncio
    # asyncio.run(nltosql_agent("每个老师有几名学生"))