import asyncio

from PySide2 import QtCore
from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout
from dayu_widgets.qt import MIcon
from qasync import QEventLoop
from dayu_widgets import MTheme, MFieldMixin, dayu_theme, MLineTabWidget

from gui.core.json_themes import Themes
from modules.wx_auto.interfaces.home_interface import HomeInterface
from modules.wx_auto.interfaces.setting_interface import SettingInterface
from modules.wx_auto.interfaces.virtual_chat_interface import VirtualChatInterface
from modules.wx_auto.interfaces.wx_chat_group_interface import WxChatGroupInterface


class WxMainWidget(QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(WxMainWidget, self).__init__(parent)
        # 初始化UI
        themes_items = Themes().items
        m_theme = MTheme()
        m_theme.set_theme(theme="light" if themes_items['theme_name'] == "bright" else "dark")
        # 自定义主题
        m_theme.title_color = themes_items["app_color"]["text_title"]
        m_theme.primary_text_color = themes_items["app_color"]["text_foreground"]
        m_theme.secondary_text_color = themes_items["app_color"]["text_description"]
        m_theme.background_color = themes_items["app_color"]["bg_one"]
        m_theme.background_selected_color = "#292929"
        m_theme.background_in_color = themes_items["app_color"]["bg_two"]
        m_theme.background_out_color = themes_items["app_color"]["bg_three"]
        # 应用到当前组件
        m_theme.apply(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('盘古开天辟地')
        self.setWindowIcon(MIcon("icons/logo.svg"))
        # 布局
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # 主页
        home_interface = HomeInterface()
        # 数据管理
        wx_chat_group_interface = WxChatGroupInterface()
        # 客服
        virtual_chat_interface = VirtualChatInterface()
        # 配置页
        setting_interface = SettingInterface()

        # 导航条
        self.tab_center = MLineTabWidget(alignment=QtCore.Qt.AlignLeft)
        self.tab_center.set_dayu_size(dayu_theme.medium)

        self.tab_center.add_tab(home_interface, {"text": "主页", "svg": "icons/主页.svg"})
        self.tab_center.add_tab(wx_chat_group_interface, {"text": "数据管理", "svg": "icons/wx.svg"})
        self.tab_center.add_tab(virtual_chat_interface, {"text": "客服", "svg": "icons/聊天.svg"})
        self.tab_center.add_tab(setting_interface, {"text": "设置", "svg": "alert_line.svg"})
        self.tab_center.tool_button_group.set_dayu_checked(0)

        self.main_layout.addWidget(self.tab_center)
        self.main_layout.addStretch()


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    wx_main_widget = WxMainWidget()
    # 显示窗口
    wx_main_widget.show()
    with loop:
        loop.run_forever()
