import asyncio
import time
from math import ceil
from PySide2 import QtCore
from PySide2.QtCore import QModelIndex
from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout
from dayu_widgets.qt import MIcon
from qasync import QEventLoop
from dayu_widgets import MTheme, MFieldMixin, dayu_theme, MTableModel, MSortFilterModel, MLineEdit, \
    MTableView, MPushButtonGroup, MPushButton, MMessage, MComboBox, MMenu, MLabel, MFlowLayout, MLoadingWrapper

from gui.utils.ddl_parse_util import parse_ddl
from gui.utils.run_in_background_util import run_in_background
from gui.widgets.c_pagination_bar.CPaginationBar import CPaginationBar, FlatStyle
from gui.widgets.c_table_view_widget.icons import icons


class ColumnConfig:
    def __init__(self, label, key,
                 width=100, default_filter=False, searchable=False, editable=False, selectable=False, checkable=False,
                 exclusive=True, order=None, color=None, bg_color=None, display=None, align=None, font=None, icon=None,
                 tooltip=None, size=None, data=None, edit=None, draggable=None, droppable=None):
        self.label = label  # 必填，用来读取 model后台数据结构的属性
        self.key = key  # 选填，显示在界面的该列的名字
        self.width = width  # 选填，单元格默认的宽度
        self.default_filter = default_filter  # 选填，如果有组合的filter组件，该属性默认是否显示，默认False
        self.searchable = searchable  # 选填，如果有搜索组件，该属性是否可以被搜索，默认False
        self.editable = editable  # 选填，该列是否可以双击编辑，默认False
        self.selectable = selectable  # 选填，该列是否可以双击编辑，且使用下拉列表选择。该下拉框的选项们，是通过 data 拿数据的
        self.checkable = checkable  # 选填，该单元格是否要加checkbox，默认False
        self.exclusive = exclusive  # 配合selectable，如果是可以多选的则为 False，如果是单选，则为True
        self.order = order  # 选填，初始化时，该列的排序方式, 0 升序，1 降序

        # 下面的是每个单元格的设置，主要用来根据本单元格数据，动态设置样式
        self.color = color  # QColor选填，该单元格文字的颜色，例如根据百分比数据大小，大于100%显示红色，小于100%显示绿色
        self.bg_color = bg_color  # 选填，该单元格的背景色，例如根据bool数据，True显示绿色，False显示红色
        self.display = display  # 选填，该单元显示的内容，例如数据是以分钟为单位，可以在这里给转换成按小时为单位
        self.align = align  # 选填，该单元格文字的对齐方式
        self.font = font  # 选填，该单元格文字的格式，例如加下划线、加粗等等
        self.icon = icon  # 选填，该单格元的图标，注意，当 QListView 使用图标模式时，每个item的图片也是在这里设置
        self.tooltip = tooltip  # 选填，鼠标指向该单元格时，显示的提示信息
        self.size = size  # 选填，该列的 hint size，设置
        self.data = data
        self.edit = edit
        self.draggable = draggable
        self.droppable = droppable

    def to_dict(self):
        return {
            "label": self.label,
            "key": self.key,
            "width": self.width,
            "default_filter": self.default_filter,
            "searchable": self.searchable,
            "editable": self.editable,
            "selectable": self.selectable,
            "checkable": self.checkable,
            "exclusive": self.exclusive,
            "order": self.order,
            # 下面的是每个单元格的设置，主要用来根据本单元格数据，动态设置样式
            "color": self.color,
            "bg_color": self.bg_color,
            "display": self.display,
            "align": self.align,
            "font": self.font,
            "icon": self.icon,
            "tooltip": self.tooltip,
            "size": self.size,
            "data": self.data,
            "edit": self.edit,
            "draggable": self.draggable,
            "droppable": self.droppable
        }


class TableViewWidgetAbstract(QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(TableViewWidgetAbstract, self).__init__(parent)

        self.page_number = 1  # 当前页码
        self.page_size = 5  # 每页数量
        self.total_count = 0  # 总数量
        self.total_page = 0  # 总页码
        self.conditions = {}  # 检索条件
        self.data_list = []  # 数据列表

        self.init_ui()  # 初始化UI
        self.reload_data()  # 载入数据

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
    def init_header_list(self):
        """
        表格配置初始化
        """
        # 接受DDL作为输入配置，进行转换 TODO
        # 这里最好给与默认配置
        self.header_list: list[ColumnConfig] = [
            ColumnConfig(
                label="名称",
                key="username"
            ),
            ColumnConfig(
                label="年龄",
                key="score",
                display=lambda x, y: f"{x}岁",
                color=lambda x, y: 'green' if x < 20 else 'red'
            )
        ]
        raise NotImplementedError

    def combine_header_list(self):
        """
        预制将ID合并到表格配置
        """
        # 先判断是否有ID项，如果没有就添加
        if isinstance(self.header_list, str):
            # 这是DDL模式
            fields = parse_ddl(self.header_list)
            self.header_list = []
            for field in fields:
                field_name = field['name']
                field_type = field['type']
                field_comment = field['comment']
                self.header_list.append(ColumnConfig(label=field_comment, key=field_name))
            self.header_list = [i.to_dict() for i in self.header_list]
        elif isinstance(self.header_list, list) and all(isinstance(item, dict) for item in self.header_list):
            # 是字典模式
            pass
        # 判断是否为 list[ColumnConfig]
        elif isinstance(self.header_list, list) and all(isinstance(item, ColumnConfig) for item in self.header_list):
            # 是实体模式
            self.header_list = [i.to_dict() for i in self.header_list]

        if "id" not in [x['key'] for x in self.header_list]:
            data = {
                "label": "ID",  # 显示名称
                "key": "id",  # 字段名称
                "checkable": True,  # 是否支持勾选
                "searchable": False,  # 是否支持搜索
                "draggable": False,  # 是否支持拖拽
                "droppable": False,  # 是否支持拖放
                "editable": False,  # 是否支持编辑(如果是下拉框，则无法双击编辑，只能下拉选择)
                "selectable": False,  # 是否支持下拉框选择，支持下拉框，需要数据中提供给key_list数据
                "exclusive": False,  # 下拉框选择是否单选
                "width": 40,  # 宽度
                # "font": lambda x, y: {"underline": True, "bold": True},  # 字体样式
                # "icon": MIcon(path=icons['新增.svg'], color='#65DB79'),  # 图标，可以动态图标
                # "display": lambda x, y: f"{x}",  # 显示格式化
                "order": QtCore.Qt.SortOrder.DescendingOrder,  # 排序
                # "bg_color": lambda x, y: "transparent" if x else dayu_theme.error_color,  # 背景颜色
                # "color": "#ff00ff",  # 文本颜色
            }
            self.header_list.insert(0, data)

    def init_function_button(self):
        """
        初始化功能按钮组：新增、删除、刷新······
        """
        # 按钮组
        button_group = MPushButtonGroup()
        button_group.set_button_list([
            {"text": "新增", "icon": MIcon(icons['新增.svg'], "#4CAF50"), 'dayu_type': MPushButton.DefaultType,
             'clicked': self.add_btn_slot},
            {"text": "删除", "icon": MIcon(icons['删除.svg'], "#F44336"), 'dayu_type': MPushButton.DefaultType,
             'clicked': self.delete_btn_slot},
            {"text": "刷新", "icon": MIcon(icons['刷新.svg'], "#03A9F4"), 'dayu_type': MPushButton.DefaultType,
             'clicked': self.reload_data},
        ])
        self.function_button_layout = QHBoxLayout()
        self.function_button_layout.addWidget(button_group)
        self.function_button_layout.addStretch()

    def init_search_bar(self):
        """
        条件筛选栏初始化
        """
        self.search_bar_layout = MFlowLayout()
        self.search_bar_layout.setContentsMargins(0, 0, 0, 0)
        for head in self.header_list:
            if 'searchable' in head and head['searchable']:
                if 'selectable' in head and head['selectable']:
                    # 下拉框
                    q_widget = QWidget()
                    layout = QHBoxLayout(q_widget)
                    layout.setContentsMargins(0, 0, 0, 0)
                    layout.setSpacing(0)
                    combo_box = MComboBox().small()
                    combo_box.set_placeholder(head['label'])
                    total_count, data_list = self.select_api(1, 1)

                    selections = []
                    if total_count > 0 and len(data_list):
                        selections = data_list[0][f"{head['key']}_list"]
                    menu = MMenu(parent=combo_box)
                    menu.set_data(selections)
                    combo_box.set_menu(menu)

                    combo_box.sig_value_changed.connect(lambda value, h=head: self.conditions.update({h['key']: value}))
                    combo_box.sig_value_changed.connect(self.reload_data)
                    if 'width' in head:
                        combo_box.setMinimumWidth(head['width'])
                    layout.addWidget(MLabel(head['label']))
                    layout.addWidget(combo_box)

                    self.search_bar_layout.addWidget(q_widget)
                else:
                    # 输入搜索
                    q_widget = QWidget()
                    layout = QHBoxLayout(q_widget)
                    layout.setContentsMargins(0, 0, 0, 0)
                    layout.setSpacing(0)
                    layout.addWidget(MLabel(head['label']))
                    edit__small = MLineEdit().small()
                    edit__small.set_delay_duration(2000)
                    edit__small.textChanged.connect(lambda value, h=head: self.conditions.update({h['key']: value}))
                    edit__small.textChanged.connect(self.reload_data)
                    if 'width' in head:
                        edit__small.setMinimumWidth(head['width'])
                    layout.addWidget(edit__small)

                    self.search_bar_layout.addWidget(q_widget)

    def init_table_view(self):
        """
        初始化表格
        """
        self.table_widget = QWidget()
        layout = QVBoxLayout(self.table_widget)
        self.combine_header_list()
        # 构建数据模型
        self.table_model = MTableModel()

        self.table_model.set_header_list(self.header_list)
        # 修改数据
        self.table_model.dataChanged.connect(self.data_changed_slot)

        # 构建排序模型
        model_sort = MSortFilterModel()
        model_sort.setSourceModel(self.table_model)
        model_sort.set_header_list(self.header_list)

        # 搜索栏
        self.search_line_edit = MLineEdit().search().small()
        self.search_line_edit.textChanged.connect(model_sort.set_search_pattern)

        # 构建表格
        self.table_view = MTableView(size=dayu_theme.small, show_row_count=False)
        self.table_view.setModel(model_sort)
        self.table_view.set_header_list(self.header_list)
        self.table_view.setShowGrid(True)
        self.table_view.enable_context_menu(True)
        layout.addWidget(self.table_view)
        # 分页控件
        self.paginationBar = CPaginationBar(self, totalPages=20)
        self.paginationBar.setInfos(f'共 {self.total_count} 条')
        # 设置扁平样式
        self.paginationBar.setStyleSheet(FlatStyle)
        self.paginationBar.pageChanged.connect(self.page_changed_slot)

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.init_header_list()  # 初始化表格配置
        self.init_function_button()  # 初始化功能组
        self.init_search_bar()  # 初始化条件筛选
        self.init_table_view()  # 初始化表格

        # 加载动画
        self.loading_wrapper = MLoadingWrapper(widget=self.table_view, loading=False)

        # 排版
        self.layout.addLayout(self.function_button_layout)  # 功能组
        self.layout.addLayout(self.search_bar_layout)  # 检索栏
        self.layout.addWidget(self.search_line_edit)  # 搜索框
        self.layout.addWidget(self.loading_wrapper)  # 动画 + 表格
        self.layout.addWidget(self.paginationBar)  # 分页卡片
        self.layout.addStretch()

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
    @run_in_background(callback=lambda self, result: self.set_data())
    def reload_data(self, *args, **kwargs):
        """
        加载数据,后台查询数据后，载入model
        :return:
        """
        self.total_page = ceil(self.total_count / self.page_size)  # 计算总页码
        # 防止超页
        if self.page_number > self.total_page and self.page_number != 1:
            self.page_number = self.total_page
        self.loading_wrapper.set_dayu_loading(True)
        self.total_count, self.data_list = self.select_api(self.page_number, self.page_size, self.conditions)

    def set_data(self):
        # 载入表格
        self.table_model.set_data_list(self.data_list)
        self.total_page = ceil(self.total_count / self.page_size)  # 计算总页码
        self.paginationBar.setTotalPages(self.total_page)
        self.paginationBar.setInfos(f'共 {self.total_count} 条')
        self.paginationBar.setCurrentPage(self.page_number)

        self.loading_wrapper.set_dayu_loading(False)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
    def page_changed_slot(self, page):
        """
        切换页码
        :param page:
        :return:
        """
        self.page_number = page
        self.reload_data()

    def data_changed_slot(self, param: QModelIndex):
        """
        编辑数据
        :param param:
        :return:
        """
        row = param.row()  # 行号
        column = param.column()  # 列号
        if param.isValid():
            model: MTableModel = param.model()  # 数据模型
            row_data = model.get_data_list()[row]  # 当前行数据，xxx_checked是否选中
            copy = row_data.copy()
            del copy['_parent']  # 去除出循环引用
            self.update_api(data=copy, id=copy['id'])

    def add_btn_slot(self):
        """
        新增数据
        :return:
        """
        self.insert_api()
        self.total_count += + 1
        self.total_page = ceil(self.total_count / self.page_size)
        self.page_number = self.total_page
        self.paginationBar.setCurrentPage(self.page_number)
        self.reload_data()

    def delete_btn_slot(self):
        """
        删除数据
        :return:
        """
        data_list = self.table_model.get_data_list()
        # 删除选中项
        checked_doc_ids = [data['id'] for data in data_list if data.get("id_checked", 0) == 2]
        if len(checked_doc_ids) == 0:
            MMessage.error("Please select the data first.", parent=self)
            return
        self.delete_api(checked_doc_ids)
        self.total_count = self.total_count - len(set(checked_doc_ids))
        self.reload_data()

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#

    def update_api(self, data, id) -> bool:
        """
        JDBC 更新API 这里根据不同的数据库类型，执行不同的更新语句
        :param data 数据内容
        :param id 数据ID
        """
        raise NotImplementedError

    def delete_api(self, id_list: list) -> bool:
        """
        JDBC 删除API 这里根据不同的数据库类型，执行不同的删除语句
        :param id_list id列表
        """
        raise NotImplementedError

    def insert_api(self) -> bool:
        """
        JDBC 新增API 这里根据不同的数据库类型，执行不同的新增语句
        """
        default_data = {

        }
        # 新增一条默认数据，然后用户通过修改去填入数据
        raise NotImplementedError

    def select_api(self, page_number, page_size, conditions=None) -> (int, list[dict]):
        """
        JDBC 查询API 这里根据不同的数据库类型，执行不同的查询语句
        :param page_number: 页码
        :param page_size: 每页数量
        :param conditions: 查询条件{}
        :return: (总数量, 数据列表)数据列表必须字典类型的列表，且必须带有id字段（删除是根据id来删除）
        """
        raise NotImplementedError


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    demo_widget = TableViewWidgetAbstract()
    MTheme("dark").apply(demo_widget)
    # 显示窗口
    demo_widget.show()
    with loop:
        loop.run_forever()
