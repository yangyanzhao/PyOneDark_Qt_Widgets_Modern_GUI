# ///////////////////////////////////////////////////////////////
# 程序启动文件，并编辑菜单与页面之间的导航连接。
# ///////////////////////////////////////////////////////////////
import asyncio

import qasync
from gui.uis.windows.main_window.functions_main_window import *
import os
from qt_core import *
from gui.core.json_settings import Settings
from gui.uis.windows.main_window import *

# 调整QT字体DPI以适应4K显示器的高分辨率
# 如果4K监视器启用 'os.environ["QT_SCALE_FACTOR"] = "2"'
os.environ["QT_FONT_DPI"] = "96"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(Functions.set_svg_image("logo.svg")))
        # 加载 主界面
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # 加载 参数设置
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True  # 显示/隐藏调整大小边缘点
        SetupMainWindow.setup_gui(self)

        # 显示 窗口
        # ///////////////////////////////////////////////////////////////
        self.show()

    # 左侧菜单按钮已发布
    # 按钮点击时运行
    # 按objectName/btn_id检查函数
    def btn_clicked(self):
        # 获取被点击的按钮
        btn = SetupMainWindow.setup_btns(self)

        # Remove Selection If Clicked By "btn_close_left_column"
        # 如果点击“btn_close_left_column”，则删除。
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active         
        top_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        top_settings.set_active(False)

        # ***左侧菜单***

        # 主页 BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # 小部件展览 BTN
        if btn.objectName() == "btn_widgets":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 2
            MainFunctions.set_page(self, self.ui.load_pages.page_2)

        # 用户 BTN
        if btn.objectName() == "btn_add_user":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())
            # Load Page 3
            MainFunctions.set_page(self, self.ui.load_pages.page_3)

        # 用户 BTN
        if btn.objectName() == "btn_we_chat":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            MainFunctions.set_page(self, self.ui.load_pages.wx_main_page)

        # 左侧底部 信息 BTN
        if btn.objectName() == "btn_info" or btn.objectName() == "btn_close_left_column_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_info_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())
                # 显示
                MainFunctions.toggle_left_column_info(self)
            else:
                if btn.objectName() == "btn_close_left_column_info":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column_info(self)
                # 隐藏
                MainFunctions.toggle_left_column_info(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            pass
            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column_info":
                MainFunctions.set_left_column_info_menu(
                    self,
                    menu=self.ui.left_column_info.menus.menus.currentWidget(),
                    title="Info Left Column",
                    icon_path=Functions.set_svg_icon("icon_info.svg")
                )
        # 左侧底部 设置 BTN
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu=self.ui.left_column.menus.menus.currentWidget(),
                    title="Settings Left Column",
                    icon_path=Functions.set_svg_icon("icon_settings.svg")
                )

        # ***标题栏菜单***

        # 标题栏 设置 BTN
        if btn.objectName() == "btn_top_settings":
            # 菜单 展开
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)
                # 显示
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)
                # 隐藏
                MainFunctions.toggle_right_column(self)

            # 获取左侧菜单BTN
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)
            # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # 左侧菜单按钮已发布
    # 按钮释放时运行
    # 按objectName/btn_id检查函数
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)
        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # 窗口大小调整事件
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # 鼠标点击事件
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()


if __name__ == "__main__":
    # 创建主循环
    app = QApplication()

    # 创建异步事件循环
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    main_window = MainWindow()
    with loop:
        loop.run_forever()
