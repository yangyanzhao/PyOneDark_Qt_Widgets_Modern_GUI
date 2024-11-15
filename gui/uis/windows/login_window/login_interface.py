import asyncio
import sys

from PySide2.QtGui import QIcon, QPixmap, QColor, Qt, QCloseEvent, QPalette
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QFrame, QVBoxLayout, QWidget
from dayu_widgets import MTheme, MMessage, MFieldMixin, MLineEdit, MPushButton
from qasync import QEventLoop, asyncSlot

from api.auth import api_login
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from gui.uis.windows.login_window.Ui_LoginWindow import Ui_Form
from gui.images import icons
from gui.utils.data_bind_util import widget_bind_value
from gui.utils.frameless_window_wrapper import FramelessWindowWrapper
from gui.utils.theme_util import setup_main_theme


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class LoginWindow(QDialog, Ui_Form, MFieldMixin):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setupUi(self)

        setup_main_theme(self)

        self.label.setScaledContents(False)
        self.setWindowTitle('蜻蜓助手')
        self.setWindowIcon(QIcon(icons['logo.svg']))
        # 获取背景图像的尺寸
        self.background_pixmap = QPixmap(icons[f'background_0.jpg'])
        self.background_width = self.background_pixmap.width()
        self.background_height = self.background_pixmap.height()

        # 设置窗口初始大小为背景图像的尺寸
        self.resize(1066, 600)
        self.update_background()

        if not isWin11():
            color = QColor(25, 33, 42)
            self.setStyleSheet(f"LoginWindow{{background: {color.name()}}}")

        self.pushButton.clicked.connect(self.on_login)
        self.logged_in = False

        # 数据绑定(账号)
        self.lineEdit_3.set_delay_duration(millisecond=2000)  # 延迟时间（毫秒
        widget_bind_value(parent=self, widget=self.lineEdit_3, field_name="login_username", widget_property="text",
                          widget_signal="textChanged")
        # 数据绑定(记住密码)
        widget_bind_value(parent=self, widget=self.checkBox, field_name="login_remember_me", widget_property="checked",
                          widget_signal="toggled")
        # 退出登录按钮
        self.quit_button = MPushButton(text='退出登录')
        self.quit_button.clicked.connect(lambda: self.on_logout(self.wrapper))
        self.quit_button.setVisible(False)
        self.verticalLayout_2.addWidget(self.quit_button)
        if self.checkBox.isChecked():
            # 数据绑定(密码)
            self.lineEdit_4.set_delay_duration(millisecond=2000)  # 延迟时间（毫秒
            widget_bind_value(parent=self, widget=self.lineEdit_4, field_name="login_password",
                              widget_property="text", widget_signal="textChanged")
        # 构建一个隐藏的LineEdit来放置Token，以后调试直接显示出来很方便。
        self.line_edit_token = MLineEdit()
        self.line_edit_token.setVisible(False)
        self.verticalLayout_2.addWidget(self.line_edit_token)
        # 数据绑定(Token)
        self.line_edit_token.set_delay_duration(millisecond=2000)  # 延迟时间（毫秒
        widget_bind_value(parent=self, widget=self.line_edit_token, field_name="login_token",
                          widget_property="text", widget_signal="textChanged")
        self.check_token()

    def set_wrapper(self, wrapper):
        self.wrapper = wrapper

    @asyncSlot()
    async def on_login(self):
        host = self.lineEdit.text()
        port = self.lineEdit_2.text()
        username = self.lineEdit_3.text()
        password = self.lineEdit_4.text()
        result = api_login(username, password)
        if result['code'] == 200:
            self.logged_in = True
            MMessage.success(result['msg'], parent=self.wrapper)
            # 写入Token
            self.line_edit_token.setText(result['token'])
            # TODO 写入用户数据
            print(result)
            self.check_token()
        else:
            MMessage.error("登录失败", parent=self.wrapper)

    @asyncSlot()
    async def on_logout(self, parent):
        # 清除Token
        self.line_edit_token.setText(None)
        self.check_token()
        MMessage.success("退出成功", parent=parent)

    def check_token(self):
        # 检测Token有效性
        token = self.line_edit_token.text()
        if token and True:  # 这里要进行API调用验证TODO
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
            return False

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.update_background()

    def update_background(self):
        """
        设置背景图
        :return:
        """
        # 获取当前窗口的尺寸
        window_width = self.width()
        window_height = self.height()

        # 计算缩放比例
        scale_width = window_width / self.background_width
        scale_height = window_height / self.background_height
        scale = max(scale_width, scale_height)

        # 根据缩放比例调整背景图像的尺寸
        scaled_width = int(self.background_width * scale)
        scaled_height = int(self.background_height * scale)
        scaled_pixmap = self.background_pixmap.scaled(scaled_width, scaled_height)
        # 设置背景图像
        self.label.setPixmap(scaled_pixmap)

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
    login_window_wrapper = FramelessWindowWrapper(target_widget=login_window, has_title_bar=True,
                                                  attach_title_bar_layout=login_window.verticalLayout_1)
    login_window_wrapper.show()
    with loop:
        loop.run_forever()
