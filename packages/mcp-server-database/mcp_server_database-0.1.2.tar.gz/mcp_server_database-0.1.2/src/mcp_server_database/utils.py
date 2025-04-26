import json
import re
from typing import List, Any
from llama_index.core import SQLDatabase

def extract_json(text):
    """提取JSON数据"""
    match = re.search(r'\{[\s\S]*?\}', text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None
    return None


def extract_table_info(tables: List[str]) -> List[any]:
    table_info = []
    for table_str in tables:
        info = {
            'table_name': '',
            'comment': '',
            'primary_keys': [],
            'foreign_keys': []
        }

        # 提取表名
        table_name_start = table_str.find("Table '") + len("Table '")
        table_name_end = table_str.find("'", table_name_start)
        info['table_name'] = table_str[table_name_start:table_name_end]

        # 提取描述（注释）
        comment_start = table_str.find("comment: (")
        if comment_start != -1:
            comment_start += len("comment: (")
            comment_end = table_str.find(")", comment_start)
            info['comment'] = table_str[comment_start:comment_end]

        # 提取主键（假设名为id或{table_name}_id的列是主键）
        columns_start = table_str.find("columns: ") + len("columns: ")
        columns_end = table_str.find(", and foreign keys:") if "foreign keys" in table_str else len(table_str)
        columns_part = table_str[columns_start:columns_end]

        # 检查是否有名为id或{table_name}_id的列
        columns = [col.strip().split()[0] for col in columns_part.split(",") if col.strip()]
        possible_pks = [col for col in columns if col == 'id' or col == f"{info['table_name'].lower()}_id"]
        if possible_pks:
            info['primary_keys'] = possible_pks

        # 提取外键
        fk_start = table_str.find("foreign keys: [")
        if fk_start != -1:
            fk_start += len("foreign keys: [")
            fk_end = table_str.find("]", fk_start)
            fk_columns = table_str[fk_start:fk_end].replace("'", "").split(", ")

            ref_table_start = table_str.find("-> ") + len("-> ")
            ref_table_end = table_str.find(".", ref_table_start)
            ref_table = table_str[ref_table_start:ref_table_end]

            ref_column_start = table_str.find("[", ref_table_end) + 1
            ref_column_end = table_str.find("]", ref_column_start)
            ref_columns = table_str[ref_column_start:ref_column_end].replace("'", "").split(", ")

            for fk_col, ref_col in zip(fk_columns, ref_columns):
                # info['foreign_keys'].append({
                #     'column': fk_col,
                #     'references': {
                #         'table': ref_table,
                #         'column': ref_col
                #     }
                # })
                info['foreign_keys'].append(fk_col)

        table_info.append(info)
    return table_info

def database_ddl(tables: List[str], sql_database: SQLDatabase) -> List[any]:
    """数据库代理"""
    tables_info = [sql_database.get_single_table_info(table) for table in tables]
    return tables_info