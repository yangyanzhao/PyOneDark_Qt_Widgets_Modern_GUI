import asyncio

from PySide2 import QtWidgets
from PySide2.QtCore import QTime
from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout
from dayu_widgets.qt import MIcon, MPixmap
from qasync import QEventLoop
from dayu_widgets import MTheme, MLineEdit, \
    MFieldMixin, MToolButton, MSwitch, MSpinBox, MTimeEdit

from gui.core.functions import Functions
from gui.core.json_themes import Themes
from gui.utils.start_up_manager import StartupManager
from gui.utils.window_task_manager import create_startup_task, create_shutdown_task, delete_task, check_task_status, \
    get_task_next_run_time, create_startup_current_program_task
from modules.wx_auto.database.settings_widget import MSettingsWidget, MSettingMeta
from modules.wx_auto.icons import icons


class SettingBaseInterface(QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(SettingBaseInterface, self).__init__(parent)
        # 初始化UI
        themes_items = Themes().items
        m_theme = MTheme()
        m_theme.set_theme(theme="light" if themes_items['theme_name'] == "bright" else "dark")
        # 自定义主题
        m_theme.title_color = themes_items["app_color"]["text_title"]
        m_theme.primary_text_color = themes_items["app_color"]["text_foreground"]
        m_theme.secondary_text_color = themes_items["app_color"]["text_description"]

        m_theme.background_color = themes_items["app_color"]["bg_one"]
        m_theme.background_selected_color = "#292929"
        m_theme.background_in_color = themes_items["app_color"]["bg_two"]
        m_theme.background_out_color = themes_items["app_color"]["bg_three"]
        # 应用到当前组件
        m_theme.apply(self)
        # 初始化UI
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('设置')
        self.setWindowIcon(MIcon(path=icons['配置.svg']))

        right_lay = QtWidgets.QVBoxLayout()
        right_lay.setContentsMargins(5, 5, 5, 5)
        right_lay.setSpacing(0)

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
        main_lay.setContentsMargins(5, 5, 5, 5)
        main_lay.setSpacing(0)

        main_lay.addWidget(splitter)
        self.setLayout(main_lay)

        self.task_card_lay = QtWidgets.QVBoxLayout()
        self.task_card_lay.setContentsMargins(5, 5, 5, 5)
        self.task_card_lay.setSpacing(5)
        task_widget.setLayout(self.task_card_lay)
        # 是否开机自启动
        meta_startup = MSettingMeta(50)
        meta_startup.setup_data({
            'avatar': MPixmap(Functions.set_svg_icon('开机自启-copy.svg')),
            # 头像图片路径 例:MPixmap("success_line.svg")
            'title': "程序开机自启",  # 标题文本
            # 'description': "开机自启动程序",  # 描述文本
        })
        m_switch_startup = MSwitch()
        m_switch_startup.setChecked(StartupManager.check_startup_status())

        def toggled_handle_startup(x):
            if x:
                StartupManager.add_to_startup()
                meta_startup._avatar.set_dayu_image(
                    MPixmap(Functions.set_svg_icon('开机自启-copy.svg'), color='yellow'))
            else:
                StartupManager.remove_from_startup()
                meta_startup._avatar.set_dayu_image(
                    MPixmap(Functions.set_svg_icon('开机自启-copy.svg'), color='#909090'))

        toggled_handle_startup(m_switch_startup.isChecked())
        m_switch_startup.toggled.connect(toggled_handle_startup)
        meta_startup.add_widget(m_switch_startup)
        self.task_card_lay.addWidget(meta_startup)

        # Windows 定时开机时间
        meta_win_open = MSettingMeta(80)
        meta_win_open.setup_data({
            'avatar': MPixmap(Functions.set_svg_icon('app-windos.svg')),
            # 头像图片路径 例:MPixmap("success_line.svg")
            'title': "电脑定时开机",  # 标题文本
            # 'description': "开机自启动程序",  # 描述文本
        })
        m_switch_win_open = MSwitch()
        status_open = check_task_status(task_name="DailyStartup")
        m_switch_win_open.setChecked(status_open)
        m_time_edit_open = MTimeEdit()

        def toggled_handle_open(x):
            if x:
                create_startup_task(task_name="DailyStartup", time=f"2023-10-01T{m_time_edit_open.text()}")
                m_time_edit_open.setDisabled(True)
                meta_win_open._avatar.set_dayu_image(
                    MPixmap(Functions.set_svg_icon('app-windos.svg'), color='green'))
            else:
                delete_task(task_name="DailyStartup")
                m_time_edit_open.setDisabled(False)
                meta_win_open._avatar.set_dayu_image(
                    MPixmap(Functions.set_svg_icon('app-windos.svg'), color='#909090'))

        if m_switch_win_open.isChecked():
            meta_win_open._avatar.set_dayu_image(
                MPixmap(Functions.set_svg_icon('app-windos.svg'), color='green'))
        else:
            meta_win_open._avatar.set_dayu_image(
                MPixmap(Functions.set_svg_icon('app-windos.svg'), color='#909090'))
        m_switch_win_open.toggled.connect(toggled_handle_open)
        meta_win_open.add_widget(m_switch_win_open)
        if status_open:
            time_open = get_task_next_run_time("DailyStartup")
            m_time_edit_open.setTime(
                QTime(time_open.hour, time_open.minute, time_open.second, time_open.microsecond // 1000))
        else:
            m_time_edit_open.setTime(QTime.currentTime())
        if m_switch_win_open.isChecked():
            m_time_edit_open.setDisabled(True)
        meta_win_open._button_layout.addWidget(m_time_edit_open)
        meta_win_open._button_layout.setContentsMargins(50, 0, 50, 0)
        self.task_card_lay.addWidget(meta_win_open)

        # Windows 定时关机时间
        meta_win_close = MSettingMeta(80)
        meta_win_close.setup_data({
            'avatar': MPixmap(Functions.set_svg_icon('app-windos.svg'), color='red'),
            # 头像图片路径 例:MPixmap("success_line.svg")
            'title': "电脑定时关机",  # 标题文本
            # 'description': "开机自启动程序",  # 描述文本
        })
        m_switch_win_close = MSwitch()
        status_close = check_task_status(task_name="DailyShutdown")
        m_switch_win_close.setChecked(status_close)
        m_time_edit_close = MTimeEdit()

        def toggled_handle_close(x):
            if x:
                create_shutdown_task(task_name="DailyShutdown", time=f"2023-10-01T{m_time_edit_close.text()}")
                m_time_edit_close.setDisabled(True)
                meta_win_close._avatar.set_dayu_image(
                    MPixmap(Functions.set_svg_icon('app-windos.svg'), color='red'))
            else:
                delete_task(task_name="DailyShutdown")
                m_time_edit_close.setDisabled(False)
                meta_win_close._avatar.set_dayu_image(
                    MPixmap(Functions.set_svg_icon('app-windos.svg'), color='#909090'))

        if m_switch_win_close.isChecked():
            meta_win_close._avatar.set_dayu_image(
                MPixmap(Functions.set_svg_icon('app-windos.svg'), color='red'))
        else:
            meta_win_close._avatar.set_dayu_image(
                MPixmap(Functions.set_svg_icon('app-windos.svg'), color='#909090'))
        m_switch_win_close.toggled.connect(toggled_handle_close)
        meta_win_close.add_widget(m_switch_win_close)
        if status_close:
            time_close = get_task_next_run_time("DailyShutdown")
            m_time_edit_close.setTime(
                QTime(time_close.hour, time_close.minute, time_close.second, time_close.microsecond // 1000))
        else:
            m_time_edit_close.setTime(QTime.currentTime())
        if m_switch_win_close.isChecked():
            m_time_edit_close.setDisabled(True)
        meta_win_close._button_layout.addWidget(m_time_edit_close)
        meta_win_close._button_layout.setContentsMargins(50, 0, 50, 0)
        self.task_card_lay.addWidget(meta_win_close)

        # 定时启动当前程序
        meta_current_program = MSettingMeta(80)
        meta_current_program.setup_data({
            'avatar': MPixmap(Functions.set_svg_icon('小程序.svg'), color='red'),
            'title': "程序定时启动"
        })
        m_switch_current_program = MSwitch()
        status_current_program = check_task_status(task_name="ProgramTimedStartup")
        m_switch_current_program.setChecked(status_current_program)
        m_time_edit_current_program = MTimeEdit()

        def toggled_handle_current_program(x):
            if x:
                create_startup_current_program_task(task_name="ProgramTimedStartup", time=f"2023-10-01T{m_time_edit_current_program.text()}")
                m_time_edit_current_program.setDisabled(True)
                meta_current_program._avatar.set_dayu_image(
                    MPixmap(Functions.set_svg_icon('小程序.svg'), color='#007DC3'))
            else:
                delete_task(task_name="ProgramTimedStartup")
                m_time_edit_current_program.setDisabled(False)
                meta_current_program._avatar.set_dayu_image(
                    MPixmap(Functions.set_svg_icon('小程序.svg'), color='#909090'))

        if m_switch_current_program.isChecked():
            meta_current_program._avatar.set_dayu_image(
                MPixmap(Functions.set_svg_icon('小程序.svg'), color='#007DC3'))
        else:
            meta_current_program._avatar.set_dayu_image(
                MPixmap(Functions.set_svg_icon('小程序.svg'), color='#909090'))
        m_switch_current_program.toggled.connect(toggled_handle_current_program)
        meta_current_program.add_widget(m_switch_current_program)
        if status_current_program:
            time_current_program = get_task_next_run_time("ProgramTimedStartup")
            m_time_edit_current_program.setTime(
                QTime(time_current_program.hour, time_current_program.minute, time_current_program.second, time_current_program.microsecond // 1000))
        else:
            m_time_edit_current_program.setTime(QTime.currentTime())
        if m_switch_current_program.isChecked():
            m_time_edit_current_program.setDisabled(True)
        meta_current_program._button_layout.addWidget(m_time_edit_current_program)
        meta_current_program._button_layout.setContentsMargins(50, 0, 50, 0)
        self.task_card_lay.addWidget(meta_current_program)

        self.task_card_lay.addStretch()


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    demo_widget = SettingBaseInterface()

    # 显示窗口
    demo_widget.show()
    loop.run_forever()
