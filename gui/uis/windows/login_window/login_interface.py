import asyncio
import random
import sys
from PySide2.QtCore import QRect
from PySide2.QtGui import QIcon, QPixmap, QColor
from PySide2.QtWidgets import QApplication, QWidget
from dayu_widgets import MTheme
from qasync import QEventLoop

from Ui_LoginWindow import Ui_Form
from gui.core.functions import Functions
from gui.images import icons


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class LoginWindow(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        MTheme().apply(self)
        self.label.setScaledContents(False)
        self.setWindowTitle('蜻蜓助手')
        self.setWindowIcon(QIcon(icons['logo.svg']))
        # 获取背景图像的尺寸
        self.background_pixmap = QPixmap(icons[f'background_0.jpg'])
        self.background_width = self.background_pixmap.width()
        self.background_height = self.background_pixmap.height()

        # 设置窗口初始大小为背景图像的尺寸
        self.resize(1066, 600)
        self.update_background()

        if not isWin11():
            color = QColor(25, 33, 42)
            self.setStyleSheet(f"LoginWindow{{background: {color.name()}}}")

        self.pushButton.clicked.connect(lambda: self.close())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.update_background()

    def update_background(self):
        """
        设置背景图
        :return:
        """
        # 获取当前窗口的尺寸
        window_width = self.width()
        window_height = self.height()

        # 计算缩放比例
        scale_width = window_width / self.background_width
        scale_height = window_height / self.background_height
        scale = max(scale_width, scale_height)

        # 根据缩放比例调整背景图像的尺寸
        scaled_width = int(self.background_width * scale)
        scaled_height = int(self.background_height * scale)
        scaled_pixmap = self.background_pixmap.scaled(scaled_width, scaled_height)
        # 设置背景图像
        self.label.setPixmap(scaled_pixmap)

    def systemTitleBarRect(self, size):
        return QRect(size.width() - 75, 0, 75, size.height())


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    login_window = LoginWindow()
    # 显示窗口
    login_window.show()
    with loop:
        loop.run_forever()
