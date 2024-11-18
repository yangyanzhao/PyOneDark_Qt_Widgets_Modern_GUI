from PySide2.QtWidgets import QLabel
from PySide2.QtCore import QTimer, Qt, QDateTime, QPropertyAnimation, QPoint, QEasingCurve
from PySide2.QtGui import QPainter, QFont

from PySide2.QtWidgets import QLabel
from PySide2.QtCore import QTimer, Qt
from PySide2.QtGui import QPainter, QTextDocument


class AnimatedLabel(QLabel):
    """
    反弹效果
    """

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setText(text)
        self.setFont(QFont("Arial", 24))
        self.setStyleSheet("color: black;")
        self.setFixedSize(400, 100)

        # 初始化动画
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(2000)
        self.animation.setStartValue(QPoint(0, 0))
        self.animation.setEndValue(QPoint(self.width() - self.fontMetrics().width(self.text()), 0))
        self.animation.setEasingCurve(QEasingCurve.Linear)

        # 设置动画循环
        self.animation.finished.connect(self.restart_animation)

    def start_animation(self):
        self.animation.start()

    def restart_animation(self):
        # 反转动画方向
        start_value = self.animation.startValue()
        end_value = self.animation.endValue()
        self.animation.setStartValue(end_value)
        self.animation.setEndValue(start_value)
        self.animation.start()


class MarqueeLabel(QLabel):
    """
    文字跑马灯
    """

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setText(text)
        # f'<span style="color: #ffff00;">{self.advertisement + "........" if self.advertisement else ""}</span>'
        self.setAlignment(Qt.AlignRight)
        self.setWordWrap(False)
        self.offset = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(100)  # 每100毫秒更新一次
        self.document = QTextDocument(self)
        self.document.setHtml(text)

    def update_text(self):
        self.offset -= 1  # 每次向左移动1个像素
        if self.offset < -self.document.idealWidth():
            self.offset = self.width()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.palette().text().color())
        painter.setFont(self.font())
        painter.translate(self.offset, 0)
        self.document.drawContents(painter, self.rect())


class DynamicTimeLabel(QLabel):
    """
    动态时钟
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次
        self.update_time()

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.setText(current_time)


class CombinedLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.marquee_label = MarqueeLabel(
            "<h1>This is a <span style='color:red;'>marquee</span> text with dynamic time: </h1>", self)
        self.time_label = DynamicTimeLabel(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(100)  # 每100毫秒更新一次

    def update_text(self):
        self.marquee_label.update_text()
        self.time_label.update_time()
        self.setText(self.marquee_label.text() + self.time_label.text())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.palette().text().color())
        painter.setFont(self.font())
        self.marquee_label.paintEvent(event)
        self.time_label.paintEvent(event)


from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.combined_label = CombinedLabel(self)
        layout.addWidget(self.combined_label)
        self.setLayout(layout)
        self.setWindowTitle("Marquee with Dynamic Time")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
