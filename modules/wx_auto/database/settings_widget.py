import asyncio
from PySide2.QtWidgets import QApplication, QWidget
from Qt import QtWidgets
from dayu_widgets import MFieldMixin, MTheme, MMeta, MSwitch
from dayu_widgets.qt import MPixmap
from qasync import QEventLoop
from tinydb import TinyDB, Query

from modules.wx_auto.database.tiny_database import table_settings, table_memory


class MSettingMeta(MMeta):
    def add_widget(self, widget):
        self._title_layout.addWidget(widget)


class MSettingsWidget(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(MSettingsWidget, self).__init__(parent)
        # 初始化UI
        self.init_ui()

    def init_ui(self):
        self.right_lay = QtWidgets.QVBoxLayout()
        self.right_lay.setContentsMargins(0, 0, 0, 0)
        self.right_lay.setSpacing(0)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        task_widget = QtWidgets.QWidget()

        scroll.setWidget(task_widget)
        self.right_lay.addWidget(scroll)
        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(self.right_lay)
        splitter = QtWidgets.QSplitter()
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 80)
        splitter.setStretchFactor(1, 20)
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.setContentsMargins(0, 0, 0, 0)
        self.main_lay.setSpacing(0)

        self.main_lay.addWidget(splitter)
        self.setLayout(self.main_lay)

        self.task_card_lay = QtWidgets.QVBoxLayout()
        task_widget.setLayout(self.task_card_lay)

    def add_setting(self, widget: QWidget, field_name: str, widget_property: str, widget_signal: str,
                    cover=None, avatar=None, title=None, description=None, extra=False, parent=None,
                    maximumHeight=None, maximumWidth=None, minimumHeight=None, minimumWidth=None):
        # 注册属性
        self.register_field(name=field_name)
        # 尝试获取配置
        field_data = table_settings.get(cond=Query()[field_name].exists())
        # 设置读取值
        if field_data and field_data[field_name]:
            self.set_field(name=field_name, value=field_data[field_name])
        else:
            self.set_field(name=field_name, value=widget.property(widget_property))
        meta = MSettingMeta()
        if maximumWidth:
            meta.setMaximumWidth(maximumWidth)
        if minimumWidth:
            meta.setMinimumWidth(minimumWidth)
        if maximumHeight:
            meta.setMaximumHeight(maximumHeight)
        if minimumHeight:
            meta.setMinimumHeight(minimumHeight)
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
        # 双向绑定
        self.bind(data_name=field_name, widget=widget, qt_property=widget_property, signal=widget_signal,
                  callback=lambda: table_settings.upsert(document={field_name: self.field(field_name)},
                                                         cond=Query()[field_name].exists()))

    @staticmethod
    def widget_bind_value(parent: MFieldMixin, widget: QWidget, field_name: str, widget_property: str,
                          widget_signal: str):
        """
        控件数据绑定数据，用来记住数据回显，使控件有记忆力。
        :param parent: 父级控件
        :param widget: 绑定控件
        :param field_name: 字段名称
        :param widget_property: 控件属性名称
        :param widget_signal: 控件的数据改变信号
        :return:
        """
        # 注册属性
        parent.register_field(name=field_name)
        # 尝试获取配置
        field_data = table_memory.get(cond=Query()[field_name].exists())
        # 设置读取值
        if field_data and field_data[field_name]:
            parent.set_field(name=field_name, value=field_data[field_name])
        else:
            parent.set_field(name=field_name, value=widget.property(widget_property))

        # 双向绑定
        parent.bind(data_name=field_name, widget=widget, qt_property=widget_property, signal=widget_signal,
                    callback=lambda: table_memory.upsert(document={field_name: parent.field(field_name)},
                                                         cond=Query()[field_name].exists()))

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
                            title="自动添加", avatar=MPixmap("user_line.svg", color="#FF0000"))
    demo_widget.add_setting(widget=MSwitch(), field_name=f"is_auto_run2", widget_property="checked",
                            widget_signal="toggled",
                            title="自动添加", avatar=MPixmap("user_line.svg", color="#FF00FF"))
    demo_widget.add_setting(widget=MSwitch(), field_name=f"is_auto_run3", widget_property="checked",
                            widget_signal="toggled",
                            title="自动添加", avatar=MPixmap("user_line.svg", color="#FFFF00"))
    MTheme(theme='dark').apply(demo_widget)
    # 显示窗口
    demo_widget.show()
    loop.run_forever()
