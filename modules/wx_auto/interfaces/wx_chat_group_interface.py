import asyncio
import functools
from math import ceil
from PySide2 import QtCore
from PySide2.QtCore import Slot, QModelIndex
from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout
from dayu_widgets.drawer import MDrawer

from dayu_widgets.qt import MIcon
from qasync import QEventLoop, asyncSlot
from dayu_widgets import MTheme, MFieldMixin, dayu_theme, MTableModel, MSortFilterModel, MLineEdit, \
    MTableView, MPushButtonGroup, MPushButton, MMessage, MLoadingWrapper, MSpinBox
from tinydb.table import Document

from modules.wx_auto.custom_widget.CPaginationBar import CPaginationBar, FlatStyle
from modules.wx_auto.database.settings_widget import MSettingsWidget
from modules.wx_auto.database.tiny_database import table_wx_chat_group_list
from modules.wx_auto.icons import icons


class WxChatGroupInterface(QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(WxChatGroupInterface, self).__init__(parent)
        self.table_wx_chat_group_list = table_wx_chat_group_list
        self.page_number = 1  # 当前页码
        self.page_size = 5  # 每页数量
        self.total_count = 0  # 总数量
        self.total_page = 0  # 总页码
        self.data_list = []  # 数据列表
        self.init_ui()
        self.reload_data()
        # 是否自动执行。
        is_auto_run = MSettingsWidget.get_setting("is_auto_run")
        if is_auto_run:
            self.start_up()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # 构建数据模型
        self.table_model = MTableModel()

        def status_color(x, y):
            if x == "未找到":
                return 'red'
            elif x == "已完成":
                return 'green'
            elif x == "未完成":
                return 'yellow'

        header_list = [
            {
                "label": "Name",
                "key": "name",
                "checkable": True,  # 是否支持勾选
                "searchable": True,  # 是否支持搜索
                "draggable": True,  # 是否支持拖拽
                "droppable": True,  # 是否支持拖放
                "editable": True,  # 是否支持编辑(如果是下拉框，则无法双击编辑，只能下拉选择)
                "selectable": False,  # 是否支持下拉框选择
                "exclusive": True,  # 下拉框选择是否单选
                "width": 200,
                "font": lambda x, y: {"underline": True, "bold": True},  # 字体样式
                "icon": MIcon(path=icons['wx.svg'], color='#65DB79'),  # 图标，可以动态图标
                "display": lambda x, y: f"{x}",  # 显示格式化
                "order": QtCore.Qt.SortOrder.DescendingOrder,  # 排序
                # "bg_color": lambda x, y: "transparent" if x else dayu_theme.error_color,  # 背景颜色
                # "color": "#ff00ff",  # 文本颜色
            },
            {
                "label": "Yield",
                "key": "yield",
                "checkable": False,  # 是否支持勾选
                "searchable": False,  # 是否支持搜索
                "draggable": False,  # 是否支持拖拽
                "droppable": False,  # 是否支持拖放
                "editable": True,  # 是否支持编辑(如果是下拉框，则无法双击编辑，只能下拉选择)
                "font": lambda x, y: {"underline": True, "bold": True},  # 字体样式
                "icon": icons['产量.svg'],  # 图标，可以动态图标
                "display": lambda x, y: f"{x}",  # 显示格式化
                "order": QtCore.Qt.SortOrder.DescendingOrder,  # 排序
                # "bg_color": lambda x, y: "transparent" if x else dayu_theme.error_color,  # 背景颜色
                # "color": "#ff00ff",  # 文本颜色
            },
            {
                "label": "状态",
                "key": "status",
                "checkable": False,  # 是否支持勾选
                "searchable": False,  # 是否支持搜索
                "draggable": False,  # 是否支持拖拽
                "droppable": False,  # 是否支持拖放
                "editable": True,  # 是否支持编辑(如果是下拉框，则无法双击编辑，只能下拉选择)
                "selectable": True,
                "font": lambda x, y: {"underline": True, "bold": True},  # 字体样式
                "icon": icons['状态.svg'],  # 图标，可以动态图标
                "display": lambda x, y: f"{x}",  # 显示格式化
                "order": QtCore.Qt.SortOrder.DescendingOrder,  # 排序
                # "bg_color": lambda x, y: "transparent" if x else dayu_theme.error_color,  # 背景颜色
                "color": status_color,  # 文本颜色
            }
        ]
        self.table_model.set_header_list(header_list)
        # 修改数据
        self.table_model.dataChanged.connect(self.data_changed_handle)

        # 构建排序模型
        self.model_sort = MSortFilterModel()
        self.model_sort.setSourceModel(self.table_model)
        self.model_sort.set_header_list(header_list)

        # 构建表格
        self.table_view = MTableView(size=dayu_theme.small, show_row_count=True)
        self.table_view.setModel(self.model_sort)
        self.table_view.set_header_list(header_list)
        self.table_view.setShowGrid(True)
        self.table_view.enable_context_menu(True)

        # 搜索栏
        line_edit = MLineEdit().search().small()
        line_edit.textChanged.connect(self.model_sort.set_search_pattern)

        # 按钮组
        button_group = MPushButtonGroup()
        button_group.set_button_list([
            {"text": "新增", "icon": MIcon(icons['新增 (1).svg'], "#4CAF50"), 'dayu_type': MPushButton.DefaultType,
             'clicked': self.add},
            {"text": "删除", "icon": MIcon(icons['删除.svg'], "#F44336"), 'dayu_type': MPushButton.DefaultType,
             'clicked': self.delete},
            {"text": "刷新", "icon": MIcon(icons['刷新.svg'], "#03A9F4"), 'dayu_type': MPushButton.DefaultType,
             'clicked': self.reload_data},
            {"text": "点赞", "icon": MIcon(icons['点赞.svg'], "#FFC107"), 'dayu_type': MPushButton.DefaultType,
             'clicked': self.thumbs_up},
            {"text": "其他", "icon": MIcon(icons['添加好友.svg'], "#8BC34A"),
             'dayu_type': MPushButton.DefaultType,
             'clicked': self.start_up}
        ])
        qh_box_layout = QHBoxLayout()
        qh_box_layout.addWidget(button_group)
        qh_box_layout.addStretch()

        # 分页控件
        self.paginationBar = CPaginationBar(self, totalPages=20)
        self.paginationBar.setInfos(f'共 {self.total_count} 条')
        # 设置扁平样式
        self.paginationBar.setStyleSheet(FlatStyle)
        self.paginationBar.pageChanged.connect(self.page_changed_handle)

        self.loading_wrapper = MLoadingWrapper(widget=self.table_view, loading=False)
        self.layout.addWidget(self.loading_wrapper)

        self.layout.addLayout(qh_box_layout)
        self.layout.addWidget(line_edit)
        self.layout.addWidget(self.table_view)
        self.layout.addWidget(self.paginationBar)
        self.layout.addStretch()

    def reload_data(self):
        """
        加载数据
        :return:
        """
        self.total_count = len(self.table_wx_chat_group_list)  # 数据总数
        self.total_page = ceil(self.total_count / self.page_size)  # 计算总页码
        # 防止超页
        if self.page_number > self.total_page:
            self.page_number = self.total_page
        self.paginationBar.setTotalPages(self.total_page)
        self.paginationBar.setInfos(f'共 {self.total_count} 条')
        self.paginationBar.setCurrentPage(self.page_number)

        # 计算起始索引
        start_index = (self.page_number - 1) * self.page_size
        self.data_list = self.table_wx_chat_group_list.all()[start_index:start_index + self.page_size]
        self.table_model.set_data_list(self.data_list)

    @Slot()
    def data_changed_handle(self, param: QModelIndex):
        """
        编辑数据
        :param param:
        :return:
        """
        row = param.row()  # 行号
        column = param.column()  # 列号
        if param.isValid():
            model: MTableModel = param.model()  # 数据模型
            row_data: Document = model.get_data_list()[row]  # 当前行数据，xxx_checked是否选中
            copy = row_data.copy()
            del copy['_parent']  # 去除出循环引用
            self.table_wx_chat_group_list.update(copy, doc_ids=[row_data.doc_id])

    def add(self):
        """
        新增数据
        :return:
        """
        self.table_wx_chat_group_list.insert({
            "name": "",
            "yield": 10,
            "status": "未完成",
            "status_list": ['未完成', '已完成', '未找到'],
        }, )
        self.total_count += + 1
        self.total_page = ceil(self.total_count / self.page_size)
        self.page_number = self.total_page
        self.paginationBar.setCurrentPage(self.page_number)
        self.reload_data()

    def delete(self):
        """
        删除数据
        :return:
        """
        data_list = self.table_model.get_data_list()
        # 删除选中项
        checked_doc_ids = [data.doc_id for data in data_list if data.get("name_checked", 0) == 2]
        if len(checked_doc_ids) == 0:
            MMessage.error("Please select the data first.", parent=self)
        self.table_wx_chat_group_list.remove(doc_ids=checked_doc_ids)
        self.reload_data()

    def page_changed_handle(self, page):
        """
        切换页码
        :param page:
        :return:
        """
        self.page_number = page
        self.reload_data()

    @asyncSlot()
    async def start_up(self, number=None):
        self.loading_wrapper.set_dayu_loading(True)
        await asyncio.sleep(1)
        self.loading_wrapper.set_dayu_loading(False)

    def thumbs_up(self):
        """
        弹窗
        :return:
        """
        self.drawer = MDrawer(parent=self.table_view, title="数量", position="right", closable=True)
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        m_spin_box_thumbs_up_number = MSpinBox()
        m_spin_box_thumbs_up_number.setRange(1, 100)
        m_spin_box_thumbs_up_number.setValue(20)
        MSettingsWidget.widget_bind_value(parent=self, widget=m_spin_box_thumbs_up_number,
                                          field_name="thumbs_up_number",
                                          widget_property="value", widget_signal="valueChanged")
        layout.addWidget(m_spin_box_thumbs_up_number)
        self.drawer.set_widget(widget)
        self.button_cancel = MPushButton("取消")
        self.button_cancel.clicked.connect(functools.partial(self.drawer.close))
        self.button_do = MPushButton("执行")
        self.button_do.clicked.connect(lambda: self.do_thumbs_up(limit=str(m_spin_box_thumbs_up_number.value())))
        self.drawer.add_widget_to_bottom(self.button_cancel)
        self.drawer.add_widget_to_bottom(self.button_do)
        self.drawer.show()

    @asyncSlot()
    async def do_thumbs_up(self, limit: str):
        self.drawer.close()


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    demo_widget = WxChatGroupInterface()
    MTheme("dark").apply(demo_widget)
    # 显示窗口
    demo_widget.show()
    with loop:
        loop.run_forever()
