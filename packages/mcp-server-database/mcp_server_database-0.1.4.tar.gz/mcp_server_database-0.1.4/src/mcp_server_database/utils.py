import json
import re
from typing import List, Any, Dict
from sqlalchemy.engine.reflection import Inspector


def extract_json(text):
    """提取JSON数据"""
    match = re.search(r"\{[\s\S]*?\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None
    return None


def extract_tables_info(inspector: Inspector) -> Dict[str, Any]:
    """
    sqlalchemy提取数据库表关键信息
    :param inspector:
    :return:
    """
    print(dir(inspector))
    # 获取数据表
    tables = inspector.get_table_names()
    # 获取表描述
    try:
        comments = inspector.get_multi_table_comment(filter_names=tables)
    except NotImplementedError:
        comments = {table: None for table in tables}
    # 获取主键
    primary_keys = inspector.get_multi_pk_constraint(filter_names=tables)
    # 获取数据表外键
    foreign_keys = inspector.get_multi_foreign_keys(filter_names=tables)

    result = {}
    for table in tables:
        # 获取表描述
        try:
            comment = comments.get((None, table), {}).get("text", "")
        except NotImplementedError:
            comment = ""
        pks = primary_keys.get((None, table), {}).get("constrained_columns", [])
        pk = pks[0] if pks else None
        # 提取外键信息并格式化
        fk_list = []
        for fk in foreign_keys.get((None, table), []):
            fk_list.extend(fk.get("constrained_columns", []))
        # 构建表信息字典
        result[table] = {"comment": comment, "primary_key": pk, "foreign_keys": fk_list}
    return result


def get_multi_table_info(inspector: Inspector, tables: List[str]) -> List[Any]:
    """sqlalchemy获取数据库表ddl"""
    tables_info = []
    for table in tables:
        res = get_single_table_info(inspector, table)
        tables.append(res)
    return tables_info


def get_single_table_info(inspector: Inspector, table_name: str) -> str:
    """提取表中的列信息"""
    template = "Table '{table_name}' has columns: {columns}, "
    try:
        table_comment = inspector.get_table_comment(table_name)["text"]
        if table_comment:
            template += f"with comment: ({table_comment}) "
    except NotImplementedError:
        print(f"注释功能在 {inspector.bind.dialect.name} 数据库中不支持，已跳过")

    template += "{foreign_keys}."
    columns = []
    for column in inspector.get_columns(table_name):
        if column.get("comment"):
            columns.append(
                f"{column['name']} ({column['type']!s}): " f"'{column.get('comment')}'"
            )
        else:
            columns.append(f"{column['name']} ({column['type']!s})")

    column_str = ", ".join(columns)
    foreign_keys = []
    for foreign_key in inspector.get_foreign_keys(table_name):
        foreign_keys.append(
            f"{foreign_key['constrained_columns']} -> "
            f"{foreign_key['referred_table']}.{foreign_key['referred_columns']}"
        )
    foreign_key_str = (
        foreign_keys and " and foreign keys: {}".format(", ".join(foreign_keys)) or ""
    )
    return template.format(
        table_name=table_name, columns=column_str, foreign_keys=foreign_key_str
    )
