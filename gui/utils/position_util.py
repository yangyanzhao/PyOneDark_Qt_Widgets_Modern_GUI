from PySide2.QtWidgets import QWidget

"""
位置工具，将当前窗口的位置位置，设定到锚定窗口的中心位置。
"""


def center_point_alignment(widget_a: QWidget, widget_current: QWidget):
    """
    將当前QWidget中心点坐标，设置为锚定QWidget中心点坐标
    :param widget_a: 锚定窗口
    :param widget_current: 当前窗口
    :return:
    """
    # 获取 widget_a 的矩形区域
    rect_a = widget_a.geometry()

    # 计算 widget_a 的中心点坐标
    center_x = rect_a.x() + rect_a.width() // 2
    center_y = rect_a.y() + rect_a.height() // 2

    # 获取 widget_b 的矩形区域
    rect_b = widget_current.geometry()

    # 计算 widget_b 的中心点坐标
    b_center_x = rect_b.width() // 2
    b_center_y = rect_b.height() // 2

    # 计算 widget_b 的新位置
    new_x = center_x - b_center_x
    new_y = center_y - b_center_y

    # 设置 widget_b 的 geometry 属性
    widget_current.setGeometry(new_x, new_y, rect_b.width(), rect_b.height())
