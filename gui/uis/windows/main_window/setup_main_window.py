# ///////////////////////////////////////////////////////////////
# 此文件，编辑菜单项、菜单图标、菜单标题、菜单位置、默认打开。
# ///////////////////////////////////////////////////////////////
from gui.core.functions import Functions
# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.widgets.py_table_widget.py_table_widget import PyTableWidget
from modules.other.widget_factory import WidgetFactory
from modules.wx_auto.interfaces.setting_interface import SettingInterface
from .functions_main_window import *
import sys
import os

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *
from .functions_main_window import MainFunctions

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from .ui_main import *

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from .functions_main_window import *
from ..left_column_menus_window.settings_base import SettingBaseInterface
from ..left_column_menus_window.user_information import UserInformationWidget
from ..left_column_menus_window.user_information_token_list import UserInformationTokenListWidget


# PY WINDOW
# ///////////////////////////////////////////////////////////////
class SetupMainWindow:
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # 添加 左侧菜单
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon": "icon_home.svg",
            "btn_id": "btn_home",
            "btn_text": "Home",
            "btn_tooltip": "Home page",
            "show_top": True,
            "is_active": True
        },
        {
            "btn_icon": "icon_widgets.svg",
            "btn_id": "btn_widgets",
            "btn_text": "Show Custom Widgets",
            "btn_tooltip": "Show custom widgets",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_add_user.svg",
            "btn_id": "btn_add_user",
            "btn_text": "Add Users",
            "btn_tooltip": "Add users",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_微信.svg",
            "btn_id": "btn_we_chat",
            "btn_text": "WeChat",
            "btn_tooltip": "Create new file",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_知乎.svg",
            "btn_id": "btn_zhi_hu",
            "btn_text": "ZhiHu",
            "btn_tooltip": "Open file",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_save.svg",
            "btn_id": "btn_save",
            "btn_text": "Save File",
            "btn_tooltip": "Save file",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_info.svg",
            "btn_id": "btn_info",
            "btn_text": "Information",
            "btn_tooltip": "Open informations",
            "show_top": False,
            "is_active": False
        },
        {
            "btn_icon": "icon_settings.svg",
            "btn_id": "btn_settings",
            "btn_text": "Settings",
            "btn_tooltip": "Open settings",
            "show_top": False,
            "is_active": False
        }
    ]

    # 添加 标题栏菜单
    # ///////////////////////////////////////////////////////////////
    add_title_bar_menus = [
        {
            "btn_icon": "icon_search.svg",
            "btn_id": "btn_search",
            "btn_tooltip": "Search",
            "is_active": False
        },
        {
            "btn_icon": "icon_settings.svg",
            "btn_id": "btn_top_settings",
            "btn_tooltip": "Top settings",
            "is_active": False
        }
    ]

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()
        elif self.ui.left_column_info.sender() != None:
            return self.ui.left_column_info.sender()

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])

        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Welcome to PyOneDark")

        # LEFT COLUMN SET SIGNALS
        # ///////////////////////////////////////////////////////////////
        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)

        self.ui.left_column_info.clicked.connect(self.btn_clicked)
        self.ui.left_column_info.released.connect(self.btn_released)

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        # ///////////////////////////////////////////////////////////////
        MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # ///////////////////////////////////////////////////////////////
        # EXAMPLE CUSTOM WIDGETS
        # Here are added the custom widgets to pages and columns that
        # were created using Qt Designer.
        # This is just an example and should be deleted when creating
        # your application.
        #
        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages
        # </OBJECTS>
        # ///////////////////////////////////////////////////////////////

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # 自定义 左列 信息菜单 TODO
        # ///////////////////////////////////////////////////////////////
        user_information_widget = UserInformationWidget(self)
        self.ui.left_column_info.menus.menus.addWidget(user_information_widget)
        self.ui.left_column_info.menus.menus.setCurrentWidget(user_information_widget)
        user_information_token_list_widget = UserInformationTokenListWidget(self)
        self.ui.left_column_info.menus.menus.addWidget(user_information_token_list_widget)
        widget_ren = WidgetFactory(widget_name="3仁")
        self.ui.left_column_info.menus.menus.addWidget(widget_ren)
        widget_yong = WidgetFactory(widget_name="4勇")
        self.ui.left_column_info.menus.menus.addWidget(widget_yong)
        widget_yan = WidgetFactory(widget_name="5严")
        self.ui.left_column_info.menus.menus.addWidget(widget_yan)
        user_information_widget.button_login_list.clicked.connect(lambda: (
            self.ui.left_column_info.menus.menus.setCurrentWidget(user_information_token_list_widget),
            user_information_token_list_widget.load_token_list(),
            user_information_widget.parent.login_window.check_token()))
        user_information_token_list_widget.personal_button.clicked.connect(
            lambda: (self.ui.left_column_info.menus.menus.setCurrentWidget(user_information_widget),user_information_widget.parent.login_window.check_token()))
        widget_ren.button.clicked.connect(lambda: self.ui.left_column_info.menus.menus.setCurrentWidget(widget_yong))
        widget_yong.button.clicked.connect(lambda: self.ui.left_column_info.menus.menus.setCurrentWidget(widget_yan))
        widget_yan.button.clicked.connect(
            lambda: self.ui.left_column_info.menus.menus.setCurrentWidget(user_information_widget))

        # 自定义 左列 设置菜单 TODO
        # ///////////////////////////////////////////////////////////////
        setting_base_interface = SettingBaseInterface()
        self.ui.left_column.menus.menus.addWidget(setting_base_interface)
        self.ui.left_column.menus.menus.setCurrentWidget(setting_base_interface)

        # 页面补全，对已有页面进行填充
        # ///////////////////////////////////////////////////////////////

        # PAGE 1 - ADD LOGO TO MAIN PAGE
        self.logo_svg = QSvgWidget(Functions.set_svg_image("logo_home.svg"))
        self.ui.load_pages.logo_layout.addWidget(self.logo_svg, Qt.AlignCenter, Qt.AlignCenter)

        # PAGE 2
        # CIRCULAR PROGRESS 1
        self.circular_progress_1 = PyCircularProgress(
            value=80,
            progress_color=self.themes["app_color"]["context_color"],
            text_color=self.themes["app_color"]["text_title"],
            font_size=14,
            bg_color=self.themes["app_color"]["dark_four"]
        )
        self.circular_progress_1.setFixedSize(200, 200)

        # CIRCULAR PROGRESS 2
        self.circular_progress_2 = PyCircularProgress(
            value=45,
            progress_width=4,
            progress_color=self.themes["app_color"]["context_color"],
            text_color=self.themes["app_color"]["context_color"],
            font_size=14,
            bg_color=self.themes["app_color"]["bg_three"]
        )
        self.circular_progress_2.setFixedSize(160, 160)

        # CIRCULAR PROGRESS 3
        self.circular_progress_3 = PyCircularProgress(
            value=75,
            progress_width=2,
            progress_color=self.themes["app_color"]["pink"],
            text_color=self.themes["app_color"]["white"],
            font_size=14,
            bg_color=self.themes["app_color"]["bg_three"]
        )
        self.circular_progress_3.setFixedSize(140, 140)

        # PY SLIDER 1
        self.vertical_slider_1 = PySlider(
            margin=8,
            bg_size=10,
            bg_radius=5,
            handle_margin=-3,
            handle_size=16,
            handle_radius=8,
            bg_color=self.themes["app_color"]["dark_three"],
            bg_color_hover=self.themes["app_color"]["dark_four"],
            handle_color=self.themes["app_color"]["context_color"],
            handle_color_hover=self.themes["app_color"]["context_hover"],
            handle_color_pressed=self.themes["app_color"]["context_pressed"]
        )
        self.vertical_slider_1.setMinimumHeight(100)

        # PY SLIDER 2
        self.vertical_slider_2 = PySlider(
            bg_color=self.themes["app_color"]["dark_three"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            handle_color=self.themes["app_color"]["context_color"],
            handle_color_hover=self.themes["app_color"]["context_hover"],
            handle_color_pressed=self.themes["app_color"]["context_pressed"]
        )
        self.vertical_slider_2.setMinimumHeight(100)

        # PY SLIDER 3
        self.vertical_slider_3 = PySlider(
            margin=8,
            bg_size=10,
            bg_radius=5,
            handle_margin=-3,
            handle_size=16,
            handle_radius=8,
            bg_color=self.themes["app_color"]["dark_three"],
            bg_color_hover=self.themes["app_color"]["dark_four"],
            handle_color=self.themes["app_color"]["context_color"],
            handle_color_hover=self.themes["app_color"]["context_hover"],
            handle_color_pressed=self.themes["app_color"]["context_pressed"]
        )
        self.vertical_slider_3.setOrientation(Qt.Horizontal)
        self.vertical_slider_3.setMaximumWidth(200)

        # PY SLIDER 4
        self.vertical_slider_4 = PySlider(
            bg_color=self.themes["app_color"]["dark_three"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            handle_color=self.themes["app_color"]["context_color"],
            handle_color_hover=self.themes["app_color"]["context_hover"],
            handle_color_pressed=self.themes["app_color"]["context_pressed"]
        )
        self.vertical_slider_4.setOrientation(Qt.Horizontal)
        self.vertical_slider_4.setMaximumWidth(200)

        # ICON BUTTON 1
        self.icon_button_1 = PyIconButton(
            icon_path=Functions.set_svg_icon("icon_heart.svg"),
            parent=self,
            app_parent=self.ui.central_widget,
            tooltip_text="Icon button - Heart",
            width=40,
            height=40,
            radius=20,
            dark_one=self.themes["app_color"]["dark_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["icon_active"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["pink"]
        )

        # ICON BUTTON 2
        self.icon_button_2 = PyIconButton(
            icon_path=Functions.set_svg_icon("icon_add_user.svg"),
            parent=self,
            app_parent=self.ui.central_widget,
            tooltip_text="BTN with tooltip",
            width=40,
            height=40,
            radius=8,
            dark_one=self.themes["app_color"]["dark_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["white"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["green"],
        )

        # ICON BUTTON 3
        self.icon_button_3 = PyIconButton(
            icon_path=Functions.set_svg_icon("icon_add_user.svg"),
            parent=self,
            app_parent=self.ui.central_widget,
            tooltip_text="BTN actived! (is_actived = True)",
            width=40,
            height=40,
            radius=8,
            dark_one=self.themes["app_color"]["dark_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["white"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["context_color"],
            is_active=True
        )

        # PUSH BUTTON 1
        self.push_button_1 = PyPushButton(
            text="Button Without Icon",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.push_button_1.setMinimumHeight(40)

        # PUSH BUTTON 2
        self.push_button_2 = PyPushButton(
            text="Button With Icon",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.icon_2 = QIcon(Functions.set_svg_icon("icon_settings.svg"))
        self.push_button_2.setMinimumHeight(40)
        self.push_button_2.setIcon(self.icon_2)

        # PY LINE EDIT
        self.line_edit = PyLineEdit(
            text="",
            place_holder_text="Place holder text",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.line_edit.setMinimumHeight(30)

        # TOGGLE BUTTON
        self.toggle_button = PyToggle(
            width=50,
            bg_color=self.themes["app_color"]["dark_two"],
            circle_color=self.themes["app_color"]["icon_color"],
            active_color=self.themes["app_color"]["context_color"]
        )

        # TABLE WIDGETS
        self.table_widget = PyTableWidget(
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["context_color"],
            bg_color=self.themes["app_color"]["bg_two"],
            header_horizontal_color=self.themes["app_color"]["dark_two"],
            header_vertical_color=self.themes["app_color"]["bg_three"],
            bottom_line_color=self.themes["app_color"]["bg_three"],
            grid_line_color=self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color=self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color=self.themes["app_color"]["dark_four"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.table_widget.setColumnCount(3)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Columns / Header
        self.column_1 = QTableWidgetItem()
        self.column_1.setTextAlignment(Qt.AlignCenter)
        self.column_1.setText("NAME")

        self.column_2 = QTableWidgetItem()
        self.column_2.setTextAlignment(Qt.AlignCenter)
        self.column_2.setText("NICK")

        self.column_3 = QTableWidgetItem()
        self.column_3.setTextAlignment(Qt.AlignCenter)
        self.column_3.setText("PASS")

        # Set column
        self.table_widget.setHorizontalHeaderItem(0, self.column_1)
        self.table_widget.setHorizontalHeaderItem(1, self.column_2)
        self.table_widget.setHorizontalHeaderItem(2, self.column_3)

        for x in range(10):
            row_number = self.table_widget.rowCount()
            self.table_widget.insertRow(row_number)  # Insert row
            self.table_widget.setItem(row_number, 0, QTableWidgetItem(str("Wanderson")))  # Add name
            self.table_widget.setItem(row_number, 1, QTableWidgetItem(str("vfx_on_fire_" + str(x))))  # Add nick
            self.pass_text = QTableWidgetItem()
            self.pass_text.setTextAlignment(Qt.AlignCenter)
            self.pass_text.setText("12345" + str(x))
            self.table_widget.setItem(row_number, 2, self.pass_text)  # Add pass
            self.table_widget.setRowHeight(row_number, 22)

        # ADD WIDGETS
        self.ui.load_pages.row_1_layout.addWidget(self.circular_progress_1)
        self.ui.load_pages.row_1_layout.addWidget(self.circular_progress_2)
        self.ui.load_pages.row_1_layout.addWidget(self.circular_progress_3)
        self.ui.load_pages.row_2_layout.addWidget(self.vertical_slider_1)
        self.ui.load_pages.row_2_layout.addWidget(self.vertical_slider_2)
        self.ui.load_pages.row_2_layout.addWidget(self.vertical_slider_3)
        self.ui.load_pages.row_2_layout.addWidget(self.vertical_slider_4)
        self.ui.load_pages.row_3_layout.addWidget(self.icon_button_1)
        self.ui.load_pages.row_3_layout.addWidget(self.icon_button_2)
        self.ui.load_pages.row_3_layout.addWidget(self.icon_button_3)
        self.ui.load_pages.row_3_layout.addWidget(self.push_button_1)
        self.ui.load_pages.row_3_layout.addWidget(self.push_button_2)
        self.ui.load_pages.row_3_layout.addWidget(self.toggle_button)
        self.ui.load_pages.row_4_layout.addWidget(self.line_edit)
        self.ui.load_pages.row_5_layout.addWidget(self.table_widget)

        # 自定义 右列 设置菜单 TODO
        # ///////////////////////////////////////////////////////////////
        widget_xq = WidgetFactory(widget_name="1象棋")
        self.ui.right_column.menus.addWidget(widget_xq)
        widget_wq = WidgetFactory(widget_name="2围棋")
        self.ui.right_column.menus.addWidget(widget_wq)
        widget_jq = WidgetFactory(widget_name="3军旗")
        self.ui.right_column.menus.addWidget(widget_jq)
        widget_tq = WidgetFactory(widget_name="4跳棋")
        self.ui.right_column.menus.addWidget(widget_tq)
        widget_dsq = WidgetFactory(widget_name="5兽棋")
        self.ui.right_column.menus.addWidget(widget_dsq)

        widget_xq.button.clicked.connect(lambda: self.ui.right_column.menus.setCurrentWidget(widget_wq))
        widget_wq.button.clicked.connect(lambda: self.ui.right_column.menus.setCurrentWidget(widget_jq))
        widget_jq.button.clicked.connect(lambda: self.ui.right_column.menus.setCurrentWidget(widget_tq))
        widget_tq.button.clicked.connect(lambda: self.ui.right_column.menus.setCurrentWidget(widget_dsq))
        widget_dsq.button.clicked.connect(lambda: self.ui.right_column.menus.setCurrentWidget(widget_xq))

        # 右列设置菜单首页（默认首页是第一个）
        self.ui.right_column.menus.setCurrentWidget(widget_xq)

        # ///////////////////////////////////////////////////////////////
        # END - EXAMPLE CUSTOM WIDGETS
        # ///////////////////////////////////////////////////////////////

    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)
