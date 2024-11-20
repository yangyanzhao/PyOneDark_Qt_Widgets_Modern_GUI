import asyncio

from PySide2.QtCore import QTime
from PySide2.QtWidgets import QApplication, QWidget, QHBoxLayout
from Qt import QtWidgets
from dayu_widgets import MTheme, MMeta, MSwitch, MTimeEdit
from dayu_widgets.collapse import MCollapse
from qasync import QEventLoop

from gui.core.json_themes import Themes
from gui.images import icons
from gui.utils.qss_utils import apply_hover_shadow_mixin
from gui.utils.start_up_manager import StartupManager
from gui.utils.window_task_manager import check_task_status, create_startup_task, delete_task, get_task_next_run_time, \
    create_shutdown_task, create_startup_current_program_task


class SettingsCollapse(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SettingsCollapse, self).__init__(parent)
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
        self._init_ui()

    def _init_ui(self):
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.setContentsMargins(5, 5, 5, 5)
        main_lay.setSpacing(0)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        m_collapse = MCollapse()
        scroll.setWidget(m_collapse)
        main_lay.addWidget(scroll)
        self.setLayout(main_lay)

        section_list = [
            {"title": "程序开机自启", "expand": False, "closable": False, "widget": self.get_program_start_up_widget()},
            {"title": "Windows 定时开机时间", "expand": False, "closable": False,
             "widget": self.get_win_timed_open_widget()},
            {"title": "Windows 定时关机时间", "expand": False, "closable": False,
             "widget": self.get_win_timed_close_widget()},
            {"title": "定时启动当前程序", "expand": False, "closable": False,
             "widget": self.get_program_timed_start_up_widget()},
        ]

        m_collapse.add_section_list(section_list)
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(m_collapse)
        main_lay.addStretch()
        m_collapse._main_layout.addStretch()

    def get_program_start_up_widget(self):
        """
        程序开机自启
        :return:
        """
        q_widget = QWidget()
        layout = QHBoxLayout(q_widget)
        # 悬停时获得阴影效果
        apply_hover_shadow_mixin(q_widget)

        m_switch_startup = MSwitch()
        m_switch_startup.setChecked(StartupManager.check_startup_status())

        def toggled_handle_startup(x):
            if x:
                StartupManager.add_to_startup()
            else:
                StartupManager.remove_from_startup()

        toggled_handle_startup(m_switch_startup.isChecked())
        m_switch_startup.toggled.connect(toggled_handle_startup)
        layout.addWidget(m_switch_startup)
        layout.addStretch()
        return q_widget

    def get_win_timed_open_widget(self):
        """
        Windows 定时开机时间
        :return:
        """
        q_widget = QWidget()
        layout = QHBoxLayout(q_widget)

        # 悬停时获得阴影效果
        apply_hover_shadow_mixin(q_widget)

        m_switch_win_open = MSwitch()
        status_open = check_task_status(task_name="DailyStartup")
        m_switch_win_open.setChecked(status_open)
        m_time_edit_open = MTimeEdit()

        def toggled_handle_open(x):
            if x:
                create_startup_task(task_name="DailyStartup", time=f"2023-10-01T{m_time_edit_open.text()}")
                m_time_edit_open.setDisabled(True)
            else:
                delete_task(task_name="DailyStartup")
                m_time_edit_open.setDisabled(False)

        m_switch_win_open.toggled.connect(toggled_handle_open)
        if status_open:
            time_open = get_task_next_run_time("DailyStartup")
            m_time_edit_open.setTime(
                QTime(time_open.hour, time_open.minute, time_open.second, time_open.microsecond // 1000))
        else:
            m_time_edit_open.setTime(QTime.currentTime())
        if m_switch_win_open.isChecked():
            m_time_edit_open.setDisabled(True)
        layout.addWidget(m_time_edit_open)
        layout.addWidget(m_switch_win_open)
        layout.addStretch()
        return q_widget

    def get_win_timed_close_widget(self):
        """
        Windows 定时关机时间
        :return:
        """
        q_widget = QWidget()
        layout = QHBoxLayout(q_widget)

        # 悬停时获得阴影效果
        apply_hover_shadow_mixin(q_widget)

        m_switch_win_close = MSwitch()
        status_close = check_task_status(task_name="DailyShutdown")
        m_switch_win_close.setChecked(status_close)
        m_time_edit_close = MTimeEdit()

        def toggled_handle_close(x):
            if x:
                create_shutdown_task(task_name="DailyShutdown", time=f"2023-10-01T{m_time_edit_close.text()}")
                m_time_edit_close.setDisabled(True)
            else:
                delete_task(task_name="DailyShutdown")
                m_time_edit_close.setDisabled(False)

        m_switch_win_close.toggled.connect(toggled_handle_close)

        if status_close:
            time_close = get_task_next_run_time("DailyShutdown")
            m_time_edit_close.setTime(
                QTime(time_close.hour, time_close.minute, time_close.second, time_close.microsecond // 1000))
        else:
            m_time_edit_close.setTime(QTime.currentTime())
        if m_switch_win_close.isChecked():
            m_time_edit_close.setDisabled(True)
        layout.addWidget(m_time_edit_close)
        layout.addWidget(m_switch_win_close)
        layout.addStretch()
        return q_widget

    def get_program_timed_start_up_widget(self):
        """
        定时启动当前程序
        :return:
        """
        q_widget = QWidget()
        layout = QHBoxLayout(q_widget)

        # 悬停时获得阴影效果
        apply_hover_shadow_mixin(q_widget)

        m_switch_current_program = MSwitch()
        status_current_program = check_task_status(task_name="ProgramTimedStartup")
        m_switch_current_program.setChecked(status_current_program)
        m_time_edit_current_program = MTimeEdit()

        def toggled_handle_current_program(x):
            if x:
                create_startup_current_program_task(task_name="ProgramTimedStartup",
                                                    time=f"2023-10-01T{m_time_edit_current_program.text()}")
                m_time_edit_current_program.setDisabled(True)
            else:
                delete_task(task_name="ProgramTimedStartup")
                m_time_edit_current_program.setDisabled(False)

        m_switch_current_program.toggled.connect(toggled_handle_current_program)

        if status_current_program:
            time_current_program = get_task_next_run_time("ProgramTimedStartup")
            m_time_edit_current_program.setTime(
                QTime(time_current_program.hour, time_current_program.minute, time_current_program.second,
                      time_current_program.microsecond // 1000))
        else:
            m_time_edit_current_program.setTime(QTime.currentTime())
        if m_switch_current_program.isChecked():
            m_time_edit_current_program.setDisabled(True)
        layout.addWidget(m_time_edit_current_program)
        layout.addWidget(m_switch_current_program)
        layout.addStretch()
        return q_widget


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)

    asyncio.set_event_loop(loop)

    # 创建窗口
    demo_widget = SettingsCollapse()

    # 显示窗口
    demo_widget.show()
    with loop:
        loop.run_forever()
