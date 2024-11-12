from PySide2.QtWidgets import QWidget
from dayu_widgets import MFieldMixin
from tinydb import Query

from modules.wx_auto.database.tiny_database import table_memory


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
