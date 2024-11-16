import asyncio
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
from Qt import QtWidgets
from dayu_widgets import MFieldMixin, MTheme, MMeta, MSwitch, MPushButton, MLabel
from dayu_widgets.mixin import hover_shadow_mixin, cursor_mixin, focus_shadow_mixin
from dayu_widgets.qt import MPixmap, get_scale_factor
from qasync import QEventLoop
from tinydb import TinyDB, Query

from gui.utils.theme_util import setup_main_theme, get_theme
from modules.wx_auto.database.tiny_database import table_settings, table_memory


@hover_shadow_mixin
@cursor_mixin
class MPanMeta(QWidget):
    """
    包装器带边缘效果
    """

    def __init__(self, widget):
        super(MPanMeta, self).__init__()
        self.layout = QVBoxLayout(self)
        self.main_layout = QVBoxLayout()
        self.center_widget = QWidget()
        self.center_widget.setLayout(self.main_layout)

        self.main_layout.addWidget(widget)
        self.layout.addWidget(self.center_widget)


class MCardListWidget(QtWidgets.QWidget):
    """
    卡片列表，带滑动条
    """

    def __init__(self, parent=None):
        super(MCardListWidget, self).__init__(parent)
        # 初始化UI
        self.init_ui()

    def init_ui(self):
        right_lay = QtWidgets.QVBoxLayout()
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        task_widget = QtWidgets.QWidget()

        scroll.setWidget(task_widget)
        right_lay.addWidget(scroll)
        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right_lay)
        splitter = QtWidgets.QSplitter()
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 80)
        splitter.setStretchFactor(1, 20)
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(splitter)
        self.setLayout(main_lay)

        self.task_card_lay = QtWidgets.QVBoxLayout()
        task_widget.setLayout(self.task_card_lay)

    def add_setting(self, widget: QWidget):
        meta = MPanMeta(widget)
        self.task_card_lay.addWidget(meta)


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # 创建窗口
    demo_widget = MCardListWidget()
    demo_widget.add_setting(widget=MPushButton("单位"))
    demo_widget.add_setting(widget=MSwitch())
    demo_widget.add_setting(widget=MLabel("黑龙江中医药大学"))
    demo_widget.task_card_lay.addStretch()
    setup_main_theme(demo_widget)
    # 显示窗口
    demo_widget.show()
    with loop:
        loop.run_forever()
