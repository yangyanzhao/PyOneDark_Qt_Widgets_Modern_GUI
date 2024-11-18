import asyncio
from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout
from dayu_widgets.qt import MIcon, MPixmap
from qasync import QEventLoop
from dayu_widgets import MTheme, MLineEdit, \
    MFieldMixin, MToolButton, MSwitch, MSpinBox

from gui.utils.theme_util import setup_main_theme
from modules.wx_auto.db.settings_widget import MSettingsWidget
from modules.wx_auto.db.tiny_db_service import TABLE_WX_CHAT_GROUP_LIST
from modules.wx_auto.icons import icons

NICKNAME = 'nickname'  # 昵称
IS_AUTO_RUN = 'is_auto_run'  # 是否自动运行
EVERY_ADD_NUMBER = 'every_add_number'  # 每次添加的数量
THUMBS_UP_NUMBER = 'thumbs_up_number'  # 数量
NOTIFY_EMAIL = 'notify_email'  # 邮箱
GREETINGS = 'greetings'


class SettingInterface(QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(SettingInterface, self).__init__(parent)
        # 初始化加载数据库
        self.table_WeChatGroupList = TABLE_WX_CHAT_GROUP_LIST
        # 初始化UI
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('设置')
        self.setWindowIcon(MIcon(path=icons['配置.svg']))
        # 布局
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        # 创建窗口
        settings_widget = MSettingsWidget()

        line_edit_name = MLineEdit()
        line_edit_name.set_prefix_widget(MToolButton().svg(icons['微信昵称.svg']).icon_only())
        line_edit_name.set_delay_duration(millisecond=2000)  # 延迟时间（毫秒）
        settings_widget.add_setting(widget=line_edit_name, field_name=NICKNAME,
                                    widget_property="text",
                                    widget_signal="textChanged",
                                    title="昵称", avatar=MPixmap(icons['微信昵称.svg'], color="#00CD66"))

        settings_widget.add_setting(widget=MSwitch(), field_name=IS_AUTO_RUN, widget_property="checked",
                                    widget_signal="toggled",
                                    title="运行", avatar=MPixmap(icons['自动运行.svg'], color="#FF0000"))

        m_spin_box_every_add_number = MSpinBox()
        m_spin_box_every_add_number.setRange(1, 100)
        m_spin_box_every_add_number.setValue(20)
        settings_widget.add_setting(widget=m_spin_box_every_add_number, field_name=EVERY_ADD_NUMBER,
                                    widget_property="value",
                                    widget_signal="valueChanged",
                                    title="数量", avatar=MPixmap(icons['好友数量.svg'], color="#FF00FF"))
        line_edit_greet = MLineEdit()
        line_edit_greet.set_prefix_widget(MToolButton().svg(icons['问候语.svg']).icon_only())
        line_edit_greet.set_delay_duration(millisecond=2000)  # 延迟时间（毫秒）
        settings_widget.add_setting(widget=line_edit_greet, field_name=GREETINGS,
                                    widget_property="text",
                                    widget_signal="textChanged",
                                    title="密钥", avatar=MPixmap(icons['问候语.svg'], color="#CCFF66"))
        self.main_layout.addWidget(settings_widget)
        line_edit_email = MLineEdit()
        line_edit_email.set_prefix_widget(MToolButton().svg(icons['邮箱.svg']).icon_only())
        line_edit_email.set_delay_duration(millisecond=2000)  # 延迟时间（毫秒）
        settings_widget.add_setting(widget=line_edit_email, field_name=NOTIFY_EMAIL,
                                    widget_property="text",
                                    widget_signal="textChanged",
                                    title="邮箱", avatar=MPixmap(icons['邮箱.svg'], color="#1E90FF"))
        self.main_layout.addWidget(settings_widget)


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    demo_widget = SettingInterface()
    setup_main_theme(demo_widget)
    # 显示窗口
    demo_widget.show()
    loop.run_forever()
