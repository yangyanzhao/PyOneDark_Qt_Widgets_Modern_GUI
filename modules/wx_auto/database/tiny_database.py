import os

from tinydb import TinyDB

from modules.wx_auto.database import current_directory

# 数据库句柄
tiny_db = TinyDB(path=os.path.join(current_directory, 'json_db.json'), ensure_ascii=False, encoding='utf-8')


# 微信群列表
table_wx_chat_group_list = tiny_db.table('WeChatGroupList')
# 提词器表
table_prompts = tiny_db.table('Prompts')
# 配置表
table_settings = tiny_db.table('Settings')
# 控件记忆表
table_memory = tiny_db.table('Memory')

# 数据表
table_demo = tiny_db.table('Demo')
