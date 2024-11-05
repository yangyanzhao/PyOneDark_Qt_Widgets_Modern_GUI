import asyncio
from PySide2.QtCore import QTimeLine, QEasingCurve, Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QVBoxLayout
from qasync import QEventLoop
class CCountUp(QLabel):
    def __init__(self, *args, **kwargs):
        super(CCountUp, self).__init__(*args, **kwargs)
        self.isFloat = False  # 是否是小数
        font = self.font() or QFont()
        font.setBold(True)
        self.setFont(font)
        self.timeline = QTimeLine(6000, self)
        self.timeline.setEasingCurve(QEasingCurve.OutExpo)
        self.timeline.frameChanged.connect(self.onFrameChanged)
    def pause(self):
        """暂停
        """
        self.timeline.setPaused(True)

    def resume(self):
        """继续
        """
        self.timeline.resume()

    def isPaused(self):
        """是否暂停
        """
        return self.timeline.state() == QTimeLine.Paused

    def reset(self):
        """重置
        """
        self.timeline.stop()
        self.isFloat = False  # 是否是小数
        self.setText('0')

    def onFrameChanged(self, value):
        if self.isFloat:
            value = round(value / 100.0 + 0.00001, 2)
        value = str(format(value, ','))
        self.setText(value + '0' if value.endswith('.0') else value)

    def setDuration(self, duration):
        """设置动画持续时间
        :param duration:
        """
        self.timeline.setDuration(duration)

    def setNum(self, number):
        """设置数字
        :param number:        int or float
        """
        if isinstance(number, int):
            self.isFloat = False
            self.timeline.setFrameRange(0, number)
        elif isinstance(number, float):
            self.isFloat = True
            self.timeline.setFrameRange(0, number * 100)
        self.timeline.stop()
        self.setText('0')
        self.timeline.start()


if __name__ == '__main__':
    # 创建主循环
    app = QApplication([])
    # 创建异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    widget = QWidget()
    layout = QVBoxLayout()
    widget.setLayout(layout)

    countLabel = CCountUp()
    countLabel.setAlignment(Qt.AlignCenter)
    countLabel.setMinimumSize(100, 100)
    countLabel.setDuration(6000)  # 动画时间 6 秒
    layout.addWidget(countLabel)

    button1 = QPushButton("开始")
    button1.clicked.connect(lambda: countLabel.setNum(1234))
    button2 = QPushButton("重置")
    button2.clicked.connect(lambda: countLabel.reset())
    button3 = QPushButton("暂停/继续")
    button3.clicked.connect(lambda: countLabel.resume() if countLabel.isPaused() else countLabel.pause())
    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(button3)
    # 显示窗口
    widget.show()
    # 显示窗口
    with loop:
        loop.run_forever()
