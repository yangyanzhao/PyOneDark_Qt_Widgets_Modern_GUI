from PySide2.QtWidgets import QWidget
from dayu_widgets import MFieldMixin
from tinydb import TinyDB, Query


# 作为数据SessionStorage存储类
class DataSessionStorage(MFieldMixin):
    def __init__(self):
        super(DataSessionStorage, self).__init__()

    def widget_bind_value(self, widget: QWidget, field_name: str, widget_property: str,
                          widget_signal: str = None, callback=None):
        """
        控件数据绑定数据，双向绑定
        :param widget: 绑定控件
        :param field_name: 字段名称（用户自定义，取名儿不要冲突）
        :param widget_property: 控件属性名称（不知道属性的，可以用后边的方法进行遍历）
        :param widget_signal: 控件的数据改变信号（不知道信号的，可以用后边的方法进行遍历），如果不传，则时单项绑定，数据绑定到控件，但是控件自身数据改变不会通过信号回传到本地数据中。
        :param callback: 数据发生改变时的主动回调，一般不传入。
        """
        data_session_storage.register_field(name=field_name)
        data_session_storage.bind(data_name=field_name, widget=widget, qt_property=widget_property,
                                  signal=widget_signal, callback=callback)


# 作为数据LocalStorage存储类,与tinydb配合使用
class DataLocalStorage(MFieldMixin):
    def __init__(self):
        super(DataLocalStorage, self).__init__()
        # 数据库句柄
        self.tiny_db = TinyDB(path='json_db.json', ensure_ascii=False, encoding='utf-8')
        # 表
        self.table_local_storage = self.tiny_db.table('LocalStorage')

    def widget_bind_value(self, widget: QWidget, field_name: str, widget_property: str,
                          widget_signal: str, callback=None):
        """
        控件数据绑定数据，用来记住数据回显，使控件有记忆力。
        :param widget: 绑定控件
        :param field_name: 字段名称（用户自定义，取名儿不要冲突）
        :param widget_property: 控件属性名称（不知道属性的，可以用后边的方法进行遍历）
        :param widget_signal: 控件的数据改变信号（不知道信号的，可以用后边的方法进行遍历）
        :param callback: 数据发生改变时的主动回调，一般不传入。
        :return:
        """
        # 注册属性
        self.register_field(name=field_name)
        # 尝试获取配置
        field_data = self.table_local_storage.get(cond=Query()[field_name].exists())
        # 设置读取值
        if field_data and field_data[field_name]:
            self.set_field(name=field_name, value=field_data[field_name])
        else:
            self.set_field(name=field_name, value=widget.property(widget_property))
        # 绑定
        if callback:
            self.bind(data_name=field_name, widget=widget, qt_property=widget_property, signal=widget_signal,
                      callback=lambda: (self.table_local_storage.upsert(document={field_name: self.field(field_name)},
                                                                        cond=Query()[field_name].exists()), callback()))
        else:
            self.bind(data_name=field_name, widget=widget, qt_property=widget_property, signal=widget_signal,
                      callback=lambda: self.table_local_storage.upsert(document={field_name: self.field(field_name)},
                                                                       cond=Query()[field_name].exists()))

    def remove(self):
        """
        移除绑定
        """
        pass


# 开局直接实例化这两个类，作为全局使用。
data_session_storage = DataSessionStorage()
data_local_storage = DataLocalStorage()
