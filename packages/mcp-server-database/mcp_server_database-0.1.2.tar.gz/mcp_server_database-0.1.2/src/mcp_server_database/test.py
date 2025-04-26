# 2. 创建 Inspector
#     inspector = inspect(engine)
#     print(dir(inspector))
#     tables = inspector.get_table_names()
#     print(type(tables), tables)
#     print(inspector.get_multi_foreign_keys(filter_names=tables))
#     # get_table_names：获取数据库表
#     # get_table_comment：获取表信息描述
#     # get_foreign_keys：获取外键信息
#     # get_multi_foreign_keys：批量获取外键信息
#     columns = inspector.get_foreign_keys("Students")
#     print(columns)