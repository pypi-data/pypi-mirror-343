from typing import List, Optional, Tuple
from urllib.parse import quote_plus

from pydantic import BaseModel, Field, model_validator
import os

from sqlalchemy import text, create_engine, Engine, inspect
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.engine.reflection import Inspector

from mcp_server_database.agent.base import BaseAgent

class CreateEngine(BaseAgent):
    """创建数据库连接引擎"""
    name: str = "engine"
    supported_databases: List[str] = Field(default=["MySQL", "PostgreSQL", "SQLite", "Oracle", "SQL Server"], description="支持的数据库类型")
    host: str = Field(None, description="数据库主机地址")
    port: int = Field(None, description="数据库端口")
    database: str = Field(None, description="数据库类型")
    user: str = Field(None, description="数据库用户名")
    password: str = Field(None, description="数据库密码")
    dbname: str = Field(None, description="数据库名称")
    engine: Optional[Engine] = None
    inspector: Optional[Inspector] = None

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    @model_validator(mode="after")
    def initialize_engine(self) -> "CreateEngine":
        """校验数据库类型是否支持"""
        self.database = os.environ.get("database").strip()
        if not self.database:
            raise ValueError("未指定数据库类型，请在环境变量中设置database")
        current_db = self.database.lower()
        support_db = [db.lower() for db in self.supported_databases]
        if current_db not in support_db:
            raise ValueError(f"仅支持一下数据库: {self.supported_databases}")
        return self

    @classmethod
    async def create(cls, **kwargs):
        """从环境变量中初始化数据库连接引擎"""
        host = os.getenv("host").strip()
        port = int(os.getenv("port").strip())
        user = os.getenv("user").strip()
        password = quote_plus(os.getenv("password")).strip()
        db_name = os.getenv("dbname").strip()
        instance = cls(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=db_name,
            engine=None,
            inspector=None,
            **kwargs
        )
        instance.engine = instance.create_engine_connect()
        if instance.engine:
            instance.inspector = inspect(instance.engine)
        return instance

    def create_engine_connect(self):
        """创建数据库连接引擎"""
        current_db = self.database.lower()
        if current_db == "mysql":
            return create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}?charset=utf8mb4")
        if current_db == "postgresql":
            return create_engine(f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}?client_encoding=utf8")
        if current_db == "sqlite":
            return create_engine(f"sqlite:///{self.dbname}")
        if current_db == "oracle":
            return create_engine(f"oracle+oracledb://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}")
        if current_db == "sql server":
            return create_engine(f"mssql+pymssql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}?charset=utf8")
        return None

    @property
    def database_type(self) -> str:
        """返回数据库类型"""
        return self.database

    def run(self, sql) -> List[Tuple]:
        """执行数据库操作"""
        try:
             with self.engine.connect() as session:
                result = session.execute(text(sql))
                return result.fetchall()
        except Exception as e:
            raise ValueError(f"执行SQL语句失败: {e}")