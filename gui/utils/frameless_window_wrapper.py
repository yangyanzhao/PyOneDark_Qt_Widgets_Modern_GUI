import asyncio
from PySide2.QtGui import Qt, QPixmap, QPalette
from PySide2.QtWidgets import QApplication, QDialog, QFrame, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QBoxLayout
from qasync import QEventLoop

from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from gui.images import icons
from gui.widgets import PyTitleBar, PyGrips

"""
窗口包装器，用于将普通窗口，包装成符合当前UI风格的边框和标题栏，标题栏位置可选择（默认为包装器顶部）。
"""


class FramelessWindowWrapper(QWidget):
    def __init__(self, target_widget: QWidget, has_title_bar=True, attach_title_bar_layout: QVBoxLayout = None):
        """
        窗口包装器
        :param target_widget: 被包装的目标窗口
        :param has_title_bar: 是否带标题栏
        :param attach_title_bar_layout: 标题附着点（默认为包装器顶部）
        """
        super().__init__()
        self.target_widget = target_widget
        self.setGeometry(self.target_widget.geometry())
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.center_widget = QWidget()
        self.center_widget.setObjectName("center_widget")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.center_widget)

        # 初始化主题和配置
        themes = Themes()
        self.themes = themes.items
        settings = Settings()
        self.settings = settings.items
        # 标题栏
        if has_title_bar:
            # 自定义标题栏
            self.title_bar_frame = QFrame()
            self.title_bar_frame.setMinimumHeight(40)
            self.title_bar_frame.setMaximumHeight(40)
            self.title_bar_layout = QVBoxLayout(self.title_bar_frame)
            self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
            # 标题栏
            self.title_bar = PyTitleBar(
                self,
                app_parent=self,
                logo_width=100,
                logo_image="logo_top_100x22.svg",
                bg_color=self.themes["app_color"]["bg_two"],
                div_color=self.themes["app_color"]["bg_three"],
                btn_bg_color=self.themes["app_color"]["bg_two"],
                btn_bg_color_hover=self.themes["app_color"]["bg_three"],
                btn_bg_color_pressed=self.themes["app_color"]["bg_one"],
                icon_color=self.themes["app_color"]["icon_color"],
                icon_color_hover=self.themes["app_color"]["icon_hover"],
                icon_color_pressed=self.themes["app_color"]["icon_pressed"],
                icon_color_active=self.themes["app_color"]["icon_active"],
                context_color=self.themes["app_color"]["context_color"],
                dark_one=self.themes["app_color"]["dark_one"],
                text_foreground=self.themes["app_color"]["text_foreground"],
                radius=8,
                radius_corners=[1, 2, 3, 4] if attach_title_bar_layout else [1, 2],
                font_family=self.settings["font"]["family"],
                title_size=self.settings["font"]["title_size"],
                is_custom_title_bar=self.settings["custom_title_bar"]
            )
            self.title_bar_layout.addWidget(self.title_bar)
            if attach_title_bar_layout is None:
                self.layout.insertWidget(0, self.title_bar_frame)
            else:
                attach_title_bar_layout.insertWidget(0, self.title_bar_frame)
        background_image = icons[f'background_0.jpg']
        background_image = f'background_0.jpg'
        style = f"""
                #center_widget {{
                    border-bottom-left-radius: 10px;
                    border-bottom-right-radius: 10px;
                    background-color: '{self.themes["app_color"]["bg_three"]}';
                }}
                """ if has_title_bar and not attach_title_bar_layout else f"""
                #center_widget {{
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                    border-bottom-left-radius: 10px;
                    border-bottom-right-radius: 10px;
                    background-color: '{self.themes["app_color"]["bg_three"]}';
                }}
                """
        self.center_widget.setStyleSheet(style)
        self.center_layout = QVBoxLayout(self)
        self.center_layout.setContentsMargins(5, 5, 5, 5)
        self.center_widget.setLayout(self.center_layout)

        # 调整边缘缩放
        self.hide_grips = True  # 显示/隐藏调整大小边缘点
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # 放置目标窗口
        self.center_layout.addWidget(target_widget)

    def resizeEvent(self, e):
        # 背景图片跟随缩放
        # self.update_background()
        super().resizeEvent(e)
        self.left_grip.setGeometry(0, 10, 10, self.height() - 5)
        self.right_grip.setGeometry(self.width() - 10, 0, 10, self.height() + 5)
        self.top_grip.setGeometry(5, 0, self.width() - 10, 10)
        self.bottom_grip.setGeometry(0, self.height() - 10, self.width() - 10, 10)

        self.top_left_grip.setGeometry(0, 0, 15, 15)
        self.top_right_grip.setGeometry(self.width() - 15, 0, 15, 15)
        self.bottom_left_grip.setGeometry(0, self.height() - 15, 15, 15)
        self.bottom_right_grip.setGeometry(self.width() - 15, self.height() - 15, 15, 15)

    # 鼠标点击事件
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()


class DemoWindow(QWidget):
    def __init__(self):
        super(DemoWindow, self).__init__()
        self.layout = QVBoxLayout(self)
        self.setGeometry(100, 100, 1000, 600)
        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()
        self.layout.addLayout(self.v_layout)
        self.layout.addLayout(self.h_layout)
        button1 = QPushButton("BTN1")
        button2 = QPushButton("BTN2")
        button3 = QPushButton("BTN3")
        self.v_layout.addWidget(button1)
        self.h_layout.addWidget(button2)
        self.h_layout.addWidget(button3)


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    demo_window = DemoWindow()
    demo_window_wrapper = FramelessWindowWrapper(target_widget=demo_window, has_title_bar=True)
    # 显示窗口
    demo_window_wrapper.show()
    with loop:
        loop.run_forever()
