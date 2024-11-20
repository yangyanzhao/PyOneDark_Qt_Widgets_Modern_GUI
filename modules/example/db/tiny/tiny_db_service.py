import os

from tinydb import TinyDB

from modules.example.db.tiny import current_directory

"""
轻量级JSON数据库
"""
# 数据库名称
TINY_DB_EXAMPLE_NAME = 'example_db.json'
# 数据库句柄
TINY_DB_EXAMPLE = TinyDB(path=os.path.join(current_directory, TINY_DB_EXAMPLE_NAME), ensure_ascii=False,
                         encoding='utf-8')

TABLE_EXAMPLE_DATA1_LIST = TINY_DB_EXAMPLE.table('Date1List')  # 示例数据表1
TABLE_EXAMPLE_DATA2_LIST = TINY_DB_EXAMPLE.table('Date2List')  # 示例数据表2
TABLE_EXAMPLE_LOCAL_STORAGE = TINY_DB_EXAMPLE.table("LocalStorage")  # LocalStorage本地存储
TABLE_EXAMPLE_SESSION_STORAGE = TINY_DB_EXAMPLE.table("SessionStorage")  # SessionStorage本地存储
