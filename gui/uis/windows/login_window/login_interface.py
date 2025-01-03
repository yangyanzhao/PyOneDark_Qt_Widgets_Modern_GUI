import asyncio
import datetime
import socket
import sys

from PySide2.QtGui import QIcon, QPixmap, QColor, Qt, QCloseEvent, QPalette
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QFrame, QVBoxLayout, QWidget
from dayu_widgets import MTheme, MMessage, MFieldMixin, MLineEdit, MPushButton
from qasync import QEventLoop, asyncSlot
from tinydb import Query

from api.auth import api_login_user, api_token_check, api_logout_user
from db.data_storage_service import py_one_dark_data_local_storage, py_one_dark_data_session_storage
from db.tiny_db_service import TABLE_PY_ONE_DARK_LOCAL_STORAGE
from gui.uis.windows.login_window.Ui_LoginWindow import Ui_Form
from gui.images import icons
from gui.uis.windows.main_window.functions_main_window import MainFunctions
from gui.utils.frameless_window_wrapper import FramelessWindowWrapper
from gui.utils.position_util import center_point_alignment
from gui.utils.qss_utils import set_label_background_image
from gui.utils.theme_util import setup_main_theme


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class LoginWindow(QDialog, Ui_Form, MFieldMixin):

    def __init__(self, parent=None):
        super().__init__()
        self.table_local_storage = TABLE_PY_ONE_DARK_LOCAL_STORAGE
        self.parent = parent
        self.setupUi(self)
        self.label.setScaledContents(False)
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.setWindowTitle('蜻蜓助手')
        self.setWindowIcon(QIcon(icons['logo.svg']))
        # 获取背景图像的尺寸
        self.background_pixmap = QPixmap(icons[f'background_0.jpg'])
        self.background_width = self.background_pixmap.width()
        self.background_height = self.background_pixmap.height()

        # 设置窗口初始大小为背景图像的尺寸
        self.resize(1066, 600)
        set_label_background_image(self.label, self.background_pixmap)

        if not isWin11():
            color = QColor(25, 33, 42)
            self.setStyleSheet(f"LoginWindow{{background: {color.name()}}}")

        self.pushButton.clicked.connect(self.on_login)
        self.logged_in = False

        # 数据绑定(账号)
        self.lineEdit_3.set_delay_duration(millisecond=2000)  # 延迟时间（毫秒
        py_one_dark_data_local_storage.widget_bind_value(widget=self.lineEdit_3, field_name="login_username",
                                                         widget_property="text",
                                                         widget_signal="textChanged")
        # 数据绑定(记住密码)
        py_one_dark_data_local_storage.widget_bind_value(widget=self.checkBox, field_name="login_remember_me",
                                                         widget_property="checked",
                                                         widget_signal="toggled")
        # 退出登录按钮
        self.quit_button = MPushButton(text='退出登录')
        self.quit_button.clicked.connect(lambda: self.on_logout(self.wrapper))
        self.quit_button.setVisible(False)
        self.verticalLayout_2.addWidget(self.quit_button)
        if self.checkBox.isChecked():
            # 数据绑定(密码)
            self.lineEdit_4.set_delay_duration(millisecond=2000)  # 延迟时间（毫秒
            py_one_dark_data_local_storage.widget_bind_value(widget=self.lineEdit_4, field_name="login_password",
                                                             widget_property="text", widget_signal="textChanged")
        # 构建一个隐藏的LineEdit来放置Token，以后调试直接显示出来很方便。
        self.line_edit_token = MLineEdit()
        self.line_edit_token.setVisible(False)
        self.verticalLayout_2.addWidget(self.line_edit_token)
        # 数据绑定(Token)
        self.line_edit_token.set_delay_duration(millisecond=2000)  # 延迟时间（毫秒
        py_one_dark_data_local_storage.widget_bind_value(widget=self.line_edit_token, field_name="login_token",
                                                         widget_property="text", widget_signal="textChanged")

    def set_wrapper(self, wrapper):
        self.wrapper = wrapper

    def on_login(self):
        host = self.lineEdit.text()
        port = self.lineEdit_2.text()
        username = self.lineEdit_3.text()
        password = self.lineEdit_4.text()
        result = api_login_user(username, password, device=socket.gethostname(), satoken=self.line_edit_token.text())
        if result['code'] == 0:
            self.logged_in = True
            MMessage.success("登录成功", parent=self)
            notify = result['msg']
            # 展示公告 TODO
            # 写入Token
            self.line_edit_token.setText(result['data']['token'])
            # 写入用户数据
            self.table_local_storage.remove(cond=Query().key == "token")
            self.table_local_storage.insert(document={"key": "token", "value": result['data']['token']})
            self.table_local_storage.remove(cond=Query().key == "user_info")
            self.table_local_storage.insert(document={"key": "user_info", "value": result['data']})
            print(result)
            self.check_token()
        else:
            MMessage.error(result['msg'], parent=self)

    @asyncSlot()
    async def on_logout(self, parent):
        logout_result = api_logout_user(satoken=self.line_edit_token.text())
        # 清除Token
        self.line_edit_token.setText(None)
        # 清除用户数据
        py_one_dark_data_session_storage.set_field("nickname", None)
        py_one_dark_data_session_storage.set_field("total_token", None)
        py_one_dark_data_session_storage.set_field("online_token", None)
        py_one_dark_data_session_storage.set_field("mobile", None)
        py_one_dark_data_session_storage.set_field("expirationDate", None)
        py_one_dark_data_session_storage.set_field("notice_information", None)
        MMessage.success("退出成功", parent=parent)
        self.check_token()

    def check_token(self):
        # 检测Token有效性
        token = self.line_edit_token.text()
        check_result = api_token_check(satoken=token)
        if token and check_result['code'] == 0:
            self.table_local_storage.remove(cond=Query().key == "user_info")
            self.table_local_storage.insert(document={"key": "user_info", "value": check_result['data']})
            # 这里要更新用户信息 TODO
            device_name = check_result['data']['token_info']['loginDevice']
            username = check_result['data']['user']['username']
            avatar = check_result['data']['user']['avatar']
            nickname = check_result['data']['user']['nickname']
            mobile = check_result['data']['user']['mobile']
            allowTokenNumber = check_result['data']['user']['allowTokenNumber']
            expirationDate = check_result['data']['user']['expirationDate']
            online_number = check_result['data']['online_number']
            msg = check_result['msg']
            py_one_dark_data_session_storage.set_field("nickname", nickname)
            py_one_dark_data_session_storage.set_field("total_token", allowTokenNumber)
            py_one_dark_data_session_storage.set_field("online_token", online_number)
            py_one_dark_data_session_storage.set_field("mobile", mobile)
            py_one_dark_data_session_storage.set_field("expirationDate",
                                                       datetime.datetime.fromtimestamp(expirationDate / 1000).strftime(
                                                           "%Y-%m-%d"))
            py_one_dark_data_session_storage.set_field("notice_information", check_result['msg'])
            # 如果有效
            self.logged_in = True
            self.lineEdit.setVisible(False)
            self.lineEdit_2.setVisible(False)
            self.lineEdit_3.setVisible(False)
            self.lineEdit_4.setVisible(False)
            self.label.setVisible(True)
            self.label_2.setVisible(True)
            self.label_3.setVisible(False)
            self.label_4.setVisible(False)
            self.label_5.setVisible(False)
            self.label_6.setVisible(False)
            self.checkBox.setVisible(False)
            self.pushButton.setVisible(False)
            self.pushButton_2.setVisible(False)
            self.quit_button.setVisible(True)
            return True
        else:
            # 如果无效
            self.logged_in = False
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
            self.lineEdit_3.setVisible(True)
            self.lineEdit_4.setVisible(True)
            self.label.setVisible(True)
            self.label_2.setVisible(True)
            self.label_3.setVisible(True)
            self.label_4.setVisible(True)
            self.label_5.setVisible(True)
            self.label_6.setVisible(True)
            self.checkBox.setVisible(True)
            self.pushButton.setVisible(True)
            self.pushButton_2.setVisible(True)
            self.quit_button.setVisible(False)
            if check_result['code'] == 100300006 or check_result['code'] == 1_003_000_01:
                # 如果Token无效则弹出登录窗口
                center_point_alignment(self.parent, self.parent.login_dialog_wrapper)
                exec_ = self.parent.login_dialog_wrapper.exec_()
                if not exec_:
                    # 回到主页
                    self.parent.ui.left_menu.select_only_one("btn_home")
                    MainFunctions.set_page(self.parent, self.parent.ui.load_pages.page_1)
            return False

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.label.setGeometry(0, 0, self.width(), self.height())
        set_label_background_image(self.label, self.background_pixmap)

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        if self.logged_in:
            self.accept()
        else:
            self.reject()
        super(LoginWindow, self).closeEvent(arg__1)


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    login_window = LoginWindow()
    setup_main_theme(login_window)
    login_window_wrapper = FramelessWindowWrapper(target_widget=login_window, has_title_bar=True,
                                                  attach_title_bar_layout=login_window.verticalLayout_1)
    login_window.set_wrapper(login_window_wrapper)
    login_window_wrapper.show()
    with loop:
        loop.run_forever()
