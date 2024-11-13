import asyncio

import qasync
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from dayu_widgets import MPushButton, MTheme


class UserInformationWidget(QWidget):
    def __init__(self, parent=None):
        self.parent = parent
        super(UserInformationWidget, self).__init__()
        MTheme(theme="dark").apply(self)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.button_logout = MPushButton(text="退出登录")
        self.button_logout.clicked.connect(self.logout)
        self.button = MPushButton(text="Click Me")
        self.button.setMaximumHeight(40)
        self.layout.addWidget(self.button_logout)
        self.layout.addWidget(self.button)

    def logout(self):
        self.parent.login_window.on_logout()


if __name__ == "__main__":
    # 创建主循环
    app = QApplication()

    # 创建异步事件循环
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    main_window = UserInformationWidget("智")
    main_window.show()
    with loop:
        loop.run_forever()
