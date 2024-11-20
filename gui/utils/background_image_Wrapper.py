import asyncio

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from dayu_widgets import MTheme
from qasync import QEventLoop
from gui.images import icons
from gui.uis.windows.login_window.login_interface import LoginWindow
from gui.utils.frameless_window_wrapper import FramelessWindowWrapper
from gui.utils.qss_utils import set_label_background_image
from gui.utils.theme_util import setup_main_theme


class BackgroundWrapper(QWidget):

    def __init__(self, source_widget: QWidget, background_image: str):
        super().__init__()
        self.source_widget = source_widget
        self.background_image = background_image
        self.source_widget.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.label = QLabel(self)
        self.label.resize(self.source_widget.width(), self.source_widget.height())
        self.label.lower()  # 将 QLabel 置于底层

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(source_widget)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.label.resize(self.width(), self.height())
        set_label_background_image(self.label, QPixmap(self.background_image))


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 原始窗口
    login_window = LoginWindow()
    setup_main_theme(login_window)
    # 背景图
    background_wrapper = BackgroundWrapper(source_widget=LoginWindow(), background_image=icons[f'background_0.jpg'])
    # 边框窗口
    frameless_window_wrapper = FramelessWindowWrapper(target_widget=background_wrapper, has_title_bar=True,
                                                      attach_title_bar_layout=background_wrapper.source_widget.verticalLayout_1)
    login_window.set_wrapper(frameless_window_wrapper)

    MTheme("dark").apply(frameless_window_wrapper)
    frameless_window_wrapper.show()
    with loop:
        loop.run_forever()
