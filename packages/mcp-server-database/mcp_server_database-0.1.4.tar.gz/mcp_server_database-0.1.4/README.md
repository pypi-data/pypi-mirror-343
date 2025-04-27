#### 简介
> 将用户的问题转化为SQL语句，然后执行SQL语句，返回结果。
 
#### 使用
```json
{
    "mcpServers": {
        "nltosql_agent": {
            "command": "uvx",
            "args": ["mcp-server-database"],
            "env": {
                "model": "模型名称",
                "api_key": "模型api_key",
                "base_url": "模型调用地址",
                "database": "数据库类型",
                "host": "数据库地址",
                "port": "数据库端口",
                "user": "数据库用户名",
                "password": "数据库密码",
                "dbname": "数据库名称"
            }
        }
    }
}
```