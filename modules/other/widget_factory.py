from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from dayu_widgets import MTheme, MPushButton


class WidgetFactory(QWidget):
    def __init__(self, widget_name):
        super(WidgetFactory, self).__init__()
        self.widget_name = widget_name
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.label = QLabel(
            f"<center><span style='font-size: 80px; color: #4F9FEE;'>{self.widget_name}</span></center>")
        self.button = MPushButton(text="Click Me")
        MTheme(theme="dark").apply(self.button)
        self.button.setMaximumHeight(40)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
