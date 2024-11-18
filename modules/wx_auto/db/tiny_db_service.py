import os

from tinydb import TinyDB

from modules.wx_auto.db import current_directory

"""
轻量级JSON数据库
"""
# 数据库名称
TINY_DB_WX_NAME = 'wx_db.json'
# 数据库句柄
TINY_DB_WX = TinyDB(path=os.path.join(current_directory, TINY_DB_WX_NAME), ensure_ascii=False, encoding='utf-8')

TABLE_WX_CHAT_GROUP_LIST = TINY_DB_WX.table('WeChatGroupList')  # 微信群列表
TABLE_WX_VIRTUAL_CHAT = TINY_DB_WX.table('VirtualChat')  # 虚拟聊天
TABLE_WX_LOCAL_STORAGE = TINY_DB_WX.table("LocalStorage")  # LocalStorage本地存储
TABLE_WX_SESSION_STORAGE = TINY_DB_WX.table("SessionStorage")  # SessionStorage本地存储
