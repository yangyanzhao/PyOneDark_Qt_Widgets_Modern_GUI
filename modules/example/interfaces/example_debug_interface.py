import asyncio
import functools
from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QListView
from dayu_widgets.qt import MIcon
from qasync import QEventLoop
from dayu_widgets import MListView, MPushButtonGroup, MPushButton, MLineEdit, \
    MFieldMixin, MLoadingWrapper, dayu_theme, MToolButton

from gui.utils.theme_util import setup_main_theme
from modules.example.icons import icons


class ExampleDebuggerInterface(QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(ExampleDebuggerInterface, self).__init__(parent)
        # 初始化UI
        self.init_ui()

    def init_ui(self):
        # 布局
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.sub_layout_button = QHBoxLayout()
        self.sub_layout_list = QVBoxLayout()
        self.main_layout.addLayout(self.sub_layout_button)
        self.main_layout.addLayout(self.sub_layout_list)
        # 按钮组
        self.button_group = MPushButtonGroup()
        self.button_group.set_button_list([
            {"text": "调试",
             "icon": MIcon(path=icons['debug.svg']),
             'dayu_type': MPushButton.DefaultType,
             'clicked': functools.partial(lambda: print())},
            {"text": "客服",
             "icon": MIcon(path=icons['客服.svg']),
             'dayu_type': MPushButton.DefaultType,
             'clicked': functools.partial(lambda: print())}
        ])
        self.sub_layout_button.addWidget(self.button_group)
        self.sub_layout_button.addStretch()
        # 搜索栏
        self.line_edit = MLineEdit().search()
        self.line_edit.set_prefix_widget(MToolButton().svg("search_line.svg").icon_only())
        # 数据栏
        self.list_view = MListView(size=dayu_theme.small)
        self.list_view.setSelectionMode(QListView.ExtendedSelection)
        self.sub_layout_list.addWidget(self.line_edit)
        self.sub_layout_list.addWidget(self.list_view)
        self.loading_wrapper = MLoadingWrapper(widget=self.list_view, loading=False)
        self.main_layout.addWidget(self.loading_wrapper)


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    demo_widget = ExampleDebuggerInterface()
    setup_main_theme(demo_widget)
    # 显示窗口
    demo_widget.show()
    with loop:
        loop.run_forever()
