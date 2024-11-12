import asyncio

import qasync
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from dayu_widgets import MPushButton, MTheme


class UserInformationWidget(QWidget):
    def __init__(self, widget_name):
        super(UserInformationWidget, self).__init__()
        self.widget_name = widget_name
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.label = QLabel(
            f"<center><span style='font-size: 80px; color: #4F9FEE;'>{self.widget_name}</span></center>")
        self.button = MPushButton(text="Click Me")
        MTheme(theme="dark").apply(self.button)
        self.button.setMaximumHeight(40)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)


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
