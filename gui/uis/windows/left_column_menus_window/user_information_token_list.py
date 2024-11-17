import qasync
from dayu_widgets import MPushButton, MLineEdit, MToolButton, MMessage
import asyncio

from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from dayu_widgets import MLabel
from tinydb import Query

from api.auth import api_login_list, api_logout_user_by_satoken
from gui.core.data_class import data_session_storage
from gui.images import icons
from gui.utils.theme_util import setup_main_theme
from modules.wx_auto.database.card_list_widget import MCardListWidget
from modules.wx_auto.database.tiny_database import table_local_storage


class TokenWidget(QWidget):
    def __init__(self, parent, device: str, token: str):
        super(TokenWidget, self).__init__()
        self.table_local_storage = table_local_storage
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.parent = parent
        self.device = device
        self.token = token

        qh_box_layout = QHBoxLayout()
        qh_box_layout.addWidget(MLabel(device))
        qh_box_layout.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(qh_box_layout)

        line_edit = MLineEdit(self)
        m_tool_button = MToolButton().svg(icons['token.svg']).icon_only()

        def tool_button_handle():
            line_edit.selectAll()
            clipboard = QApplication.clipboard()
            clipboard.setText(line_edit.selectedText())
            MMessage.success("Copied", parent=self)

        m_tool_button.clicked.connect(tool_button_handle)
        line_edit.set_prefix_widget(m_tool_button)
        line_edit.setText(token)
        self.layout.addWidget(line_edit)

        q_button_clear = MPushButton("清退")
        q_button_clear.clicked.connect(self.logout)
        self.layout.addWidget(q_button_clear)

    def logout(self):
        token_info = self.table_local_storage.get(Query().key == "token")
        api_logout_user_by_satoken(satoken=token_info['value'], logout_token=self.token)
        self.parent.load_token_list()
        if token_info['value'] == self.token:
            # 清除用户数据
            data_session_storage.set_field("nickname", None)
            data_session_storage.set_field("total_token", None)
            data_session_storage.set_field("online_token", None)
            data_session_storage.set_field("mobile", None)
            data_session_storage.set_field("expirationDate", None)


class UserInformationTokenListWidget(QWidget):
    def __init__(self, parent=None):
        super(UserInformationTokenListWidget, self).__init__(parent)
        self.table_local_storage = table_local_storage
        self.parent = parent
        self.setWindowTitle("令牌列表")
        setup_main_theme(self)
        # 布局
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        # 创建窗口
        self.token_list_widget = MCardListWidget()
        self.main_layout.addWidget(self.token_list_widget)
        self.personal_button = MPushButton("个人中心")
        self.load_token_list()

    def load_token_list(self):
        # 清空布局中的所有控件
        # 清空布局中的所有控件
        while self.token_list_widget.task_card_lay.count():
            item = self.token_list_widget.task_card_lay.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        token_info = self.table_local_storage.get(Query().key == "token")
        token_list = api_login_list(token_info['value'])
        if token_list:
            for key, value in token_list.items():
                if token_info['value'] == key:
                    # 本机
                    value = f'<span style="color: red; font-size: 16px;"><b>{value}</b></span>'
                self.token_list_widget.add_setting(
                    widget=TokenWidget(self, value, key))

        self.token_list_widget.task_card_lay.addStretch()
        self.token_list_widget.add_setting(widget=self.personal_button)


if __name__ == "__main__":
    # 创建主循环
    app = QApplication()
    # 创建异步事件循环
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    main_window = UserInformationTokenListWidget()
    token_list = [
        {'device': '电脑端', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': '手机端', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device3', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device4', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device4', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device4', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device4', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device4', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
    ]
    main_window.show()
    with loop:
        loop.run_forever()
