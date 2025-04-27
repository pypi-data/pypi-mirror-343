import os

from mcp.server.fastmcp import FastMCP
from mcp_server_database.agent.react import ReActAgent
from dotenv import load_dotenv

load_dotenv(verbose=True)

mcp = FastMCP("database")
USER_AGENT = "database/1.0"


@mcp.tool()
async def nltosql_agent(query: str) -> str:
    """
    当用户明确需要查询数据库时，使用该工具。
    该函数将用户问题经过思考、计划和执行三个步骤，最终以markdown格式返回结果。
    输入参数query：用户数据库问题，类型为字符串。
    """
    sql_agent = await ReActAgent.create()
    try:
        result = await sql_agent.query(query)
        print("最后的结果：", result)
        return result
    finally:
        await sql_agent.cleanup()


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
    # import asyncio
    # asyncio.run(nltosql_agent("collections表中有几个连接信息，分别有哪些？"))
