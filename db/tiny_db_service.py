import os

from tinydb import TinyDB

from db import current_directory

"""
轻量级JSON数据库
"""
# 数据库名称
TINY_DB_PY_ONE_DARK_NAME = 'py_one_dark_db.json'

# 数据库句柄
TINY_DB_PY_ONE_DARK = TinyDB(path=os.path.join(current_directory, TINY_DB_PY_ONE_DARK_NAME), ensure_ascii=False, encoding='utf-8')

# 数据库表集合
TABLE_PY_ONE_DARK_LOCAL_STORAGE = TINY_DB_PY_ONE_DARK.table("LocalStorage")  # LocalStorage本地存储
TABLE_PY_ONE_DARK_SESSION_STORAGE = TINY_DB_PY_ONE_DARK.table("SessionStorage")  # SessionStorage本地存储
