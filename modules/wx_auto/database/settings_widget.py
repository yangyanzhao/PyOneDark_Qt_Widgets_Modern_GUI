import asyncio
from PySide2.QtWidgets import QApplication, QWidget
from Qt import QtWidgets
from dayu_widgets import MFieldMixin, MTheme, MMeta, MSwitch
from dayu_widgets.qt import MPixmap
from qasync import QEventLoop
from tinydb import TinyDB, Query

from gui.core.data_class import data_local_storage
from gui.utils.theme_util import setup_main_theme
from modules.wx_auto.database.tiny_database import table_settings, table_memory


class MSettingMeta(MMeta):
    def __init__(self, maximumHeight=80):
        super(MSettingMeta, self).__init__()
        self.setMaximumHeight(maximumHeight)

    def add_widget(self, widget):
        self._title_layout.addWidget(widget)


class MSettingsWidget(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(MSettingsWidget, self).__init__(parent)
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

    def add_setting(self, widget: QWidget, field_name: str, widget_property: str, widget_signal: str,
                    cover=None, avatar=None, title=None, description=None, extra=False, parent=None):
        # 数据双向绑定
        data_local_storage.widget_bind_value(widget=widget,
                                             field_name=field_name,
                                             widget_property=widget_property,
                                             widget_signal=widget_signal)
        meta = MSettingMeta()
        meta.setup_data({
            'cover': cover,  # 封面图片路径 例:MPixmap("app-houdini.png")
            'avatar': avatar,  # 头像图片路径 例:MPixmap("success_line.svg")
            'title': title,  # 标题文本
            'description': description,  # 描述文本
            'extra': extra,
            'parent': parent
        })
        if widget and isinstance(widget, QWidget):
            meta.add_widget(widget)
        self.task_card_lay.addWidget(meta)

    @staticmethod
    def get_setting(field_name):
        """
        获取配置
        :param field_name:
        :return:
        """
        field_data = table_settings.get(cond=Query()[field_name].exists())
        # 设置读取值
        if field_data and field_data[field_name]:
            return field_data[field_name]


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # 创建窗口
    demo_widget = MSettingsWidget()
    demo_widget.add_setting(widget=MSwitch(), field_name=f"is_auto_run1", widget_property="checked",
                            widget_signal="toggled",
                            title="自动添加", avatar=MPixmap("icons/自动运行.svg", color="#FF0000"))
    demo_widget.add_setting(widget=MSwitch(), field_name=f"is_auto_run2", widget_property="checked",
                            widget_signal="toggled",
                            title="自动添加", avatar=MPixmap("icons/自动运行.svg", color="#FF00FF"))
    demo_widget.add_setting(widget=MSwitch(), field_name=f"is_auto_run3", widget_property="checked",
                            widget_signal="toggled",
                            title="自动添加", avatar=MPixmap("icons/自动运行.svg", color="#FFFF00"))
    setup_main_theme(demo_widget)
    # 显示窗口
    demo_widget.show()
    loop.run_forever()
