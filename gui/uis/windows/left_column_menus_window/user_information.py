import qasync
from dayu_widgets import MPushButton, MTheme
import asyncio

from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from dayu_widgets import MLabel

from gui.images import icons
from gui.utils.theme_util import setup_main_theme
from modules.wx_auto.custom_widget.CAvatar import CAvatar
from gui.utils.position_util import center_point_alignment


class InforWidget(QWidget):
    def __init__(self, avatar: CAvatar = None, name: str = None, value: str = None):
        super(InforWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        i = 0
        if avatar:
            qh_box_layout = QHBoxLayout()
            qh_box_layout.addWidget(avatar)
            qh_box_layout.setAlignment(Qt.AlignCenter)
            self.layout.addLayout(qh_box_layout)

        if name:
            q_label_name = MLabel(name)
            q_label_name.setWordWrap(True)
            q_label_name.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(q_label_name)
        if value:
            q_label_value = MLabel(value)
            q_label_value.setWordWrap(True)
            q_label_value.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(q_label_value)


class UserInformationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("个人中心")
        setup_main_theme(self)

        # 主布局-垂直
        self.main_layout = QVBoxLayout(self)
        # 头像
        self.avatar_layout = QHBoxLayout(self)
        c_avatar = CAvatar(shape=CAvatar.Rectangle, size=QSize(200, 150),
                           url='https://pic.netbian.com/uploads/allimg/231016/223346-16974668265cf4.jpg', is_OD=True,
                           animation=False, parent=self)
        self.avatar_layout.addWidget(c_avatar)
        # 部门 职务 年资
        self.post_layout = QHBoxLayout(self)
        self.post_layout.addWidget(InforWidget(
            name=f"<span style='color: #7bb8d7;font-family: KaiTi;font-size: 14px; font-weight: bold;'>部门</span>",
            value="HCP实施部"))
        self.post_layout.addWidget(InforWidget(
            name=f"<span style='color: #7bb8d7;font-family: KaiTi;font-size: 14px; font-weight: bold;'>职务</span>",
            value="经理"))
        self.post_layout.addWidget(InforWidget(
            name=f"<span style='color: #7bb8d7;font-family: KaiTi;font-size: 14px; font-weight: bold;'>年资</span>",
            value="2年"))
        self.post_layout.setStretch(0, 1)
        self.post_layout.setStretch(1, 1)
        self.post_layout.setStretch(2, 1)
        # 手机 地址
        self.phone_address_layout = QHBoxLayout(self)
        c_avatar_phone = CAvatar(shape=CAvatar.Circle, size=CAvatar.SizeSmall,
                                 url=icons['手机.svg'])
        self.phone_address_layout.addWidget(InforWidget(avatar=c_avatar_phone,
                                                        name=f"<span style='color: #808080;font-family: KaiTi;font-size: 14px;'>手机</span>",
                                                        value="13888888888"))
        c_avatar_address = CAvatar(shape=CAvatar.Circle, size=CAvatar.SizeSmall,
                                   url=icons['过期时间.svg'],animation=True)
        self.phone_address_layout.addWidget(
            InforWidget(avatar=c_avatar_address,
                        name=f"<span style='color: #808080;font-family: KaiTi;font-size: 14px;'>过期时间</span>",
                        value="2024:11:16 21:12:00"))
        self.phone_address_layout.setStretch(0, 2)
        self.phone_address_layout.setStretch(1, 3)

        self.rout_layout = QVBoxLayout(self)
        self.button_logout = MPushButton(text="登录")
        self.button_logout.clicked.connect(self.logout)
        self.rout_layout.addWidget(self.button_logout)

        self.login_list_layout = QVBoxLayout(self)
        self.button_login_list = MPushButton(text="在线列表")
        self.login_list_layout.addWidget(self.button_login_list)

        # 设置主布局
        self.setLayout(self.main_layout)
        self.main_layout.addLayout(self.avatar_layout)
        self.main_layout.addLayout(self.post_layout)
        self.main_layout.addLayout(self.phone_address_layout)
        self.main_layout.addLayout(self.rout_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.login_list_layout)

    def logout(self):
        if self.parent:
            center_point_alignment(self.parent, self.parent.login_dialog_wrapper)
            check = self.parent.login_dialog_wrapper.target_widget.check_token()
            if check:
                self.parent.login_dialog_wrapper.show()



if __name__ == "__main__":
    # 创建主循环
    app = QApplication()
    # 创建异步事件循环
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 创建窗口
    main_window = UserInformationWidget()
    main_window.show()
    with loop:
        loop.run_forever()
