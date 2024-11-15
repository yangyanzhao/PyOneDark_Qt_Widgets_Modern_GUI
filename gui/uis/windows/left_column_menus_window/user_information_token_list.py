import qasync
from dayu_widgets import MPushButton, MTheme, MFlowLayout, MTextEdit
import asyncio

from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from dayu_widgets import MLabel
from dayu_widgets.qt import MPixmap

from gui.images import icons
from gui.utils.theme_util import setup_main_theme
from modules.wx_auto.custom_widget.CAvatar import CAvatar
from gui.utils.position_util import center_point_alignment
from modules.wx_auto.database.settings_widget import MSettingsWidget


class TokenWidget(QWidget):
    def __init__(self, device: str, token: str):
        super(TokenWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        qh_box_layout = QHBoxLayout()
        qh_box_layout.addWidget(MLabel(device))
        qh_box_layout.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(qh_box_layout)

        q_text_edit = MTextEdit(self)
        q_text_edit.setText(token)
        q_text_edit.setMaximumHeight(30)
        q_text_edit.setDisabled(True)
        self.layout.addWidget(q_text_edit)

        q_button_clear = MPushButton("清退")
        self.layout.addWidget(q_button_clear)


class UserInformationTokenListWidget(QWidget):
    def __init__(self, parent=None):
        super(UserInformationTokenListWidget, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle("令牌列表")
        setup_main_theme(self)
        # 布局
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        # 创建窗口
        self.token_list_widget = MSettingsWidget()

    def setupTokenList(self, token_list: list):
        for token in token_list:
            self.token_list_widget.add_setting(widget=TokenWidget(token['device'], token['token']),
                                               title="运行", avatar=MPixmap(icons['自动运行.svg'], color="#FF0000"))
            self.main_layout.addWidget(self.token_list_widget)

    def logout(self):
        pass


if __name__ == "__main__":
    # 创建主循环
    app = QApplication()
    # 创建异步事件循环
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    main_window = UserInformationTokenListWidget()
    token_list = [
        {'device': 'device1', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device2', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device3', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device4', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device4', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device4', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device4', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
        {'device': 'device4', 'token': 'b3ff8b86-8f04-40ac-8be9-4f152329c68e'},
    ]
    main_window.setupTokenList(token_list)
    main_window.show()
    with loop:
        loop.run_forever()
