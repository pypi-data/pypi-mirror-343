#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @XZGUtil    : 2021-01-09 19:36
# @Site    :
# @File    : logger.py
# @Software: PyCharm
"""
装饰器
说明：
前景色            背景色           颜色
---------------------------------------
30                40              黑色
31                41              红色
32                42              绿色
33                43              黃色
34                44              蓝色
35                45              紫红色
36                46              青蓝色
37                47              白色
显示方式           意义
-------------------------
0                终端默认设置
1                高亮显示
4                使用下划线
5                闪烁
7                反白显示
8                不可见
"""
import datetime
import traceback
from functools import wraps
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
import atexit
import time  # 添加time导入
import sys


def logit(func):
    """
    日志输出
    :param func:
    :return:
    """

    @wraps(func)
    def with_logging(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'\033[1;31m {date} \033[0m - \033[4;33m{func.__name__}\033[0m -\033[1;35m 耗时:{"%.4f" % (t2 - t1)}秒\033[0m - \033[1;32m{result}\033[0m')
        return result

    return with_logging


def async_logit(func):
    @wraps(func)
    async def with_logging(*args, **kwargs):
        t1 = time.time()
        result = await func(*args, **kwargs)
        t2 = time.time()
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'\033[1;31m {date} \033[0m - \033[4;33m{func.__name__}\033[0m -\033[1;35m 耗时:{"%.4f" % (t2 - t1)}秒\033[0m - \033[1;32m{result}\033[0m')
        return result

    return with_logging


def conlog(*args):
    date = datetime.datetime.now().strftime('%Y%m%d/%H%M%S')
    text = ''
    for tx in args:
        text += f"{tx} "
    trc = traceback.extract_stack()[-2]
    filename = trc.filename
    str = lambda: filename.split("\\")[-1] if "\\" in filename else filename.split('/')[-1]
    str = f'\033[1;32m{date}\033[0m|\033[4;31m{str()}\033[0m|\033[1;33m{trc.name}:{trc.lineno}\033[0m|{text}'
    print(str)
    return str





class _FloatingLoggerImpl(QWidget):
    """实际的日志窗口实现类"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        atexit.register(self.cleanup)

    def _setup_ui(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(40, 40, 40, 180);
                border-radius: 5px;
            }
            QTextEdit {
                color: white;
                background: transparent;
                border: none;
                font: 10pt Consolas;
                padding: 5px;
            }
        """)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        self.resize(400, 200)
        self._move_to_bottom_right()

    def _move_to_bottom_right(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            screen.right() - self.width() - 10,
            screen.bottom() - self.height() - 40
        )

    def log_message(self, message, level="info"):
        color_map = {
            "info": "#006400",  # 深绿色
            "warning": "#FFFF00",  # 黄色
            "error": "#FF5A5A",  # 红色
            "debug": "#808080"  # 灰色
        }
        self.text_edit.append(
            f'<span style="color:{color_map.get(level, "white")}">'
            f'[{level.upper()}] {message}'
            f'</span>'
        )
        self.text_edit.verticalScrollBar().setValue(
            self.text_edit.verticalScrollBar().maximum()
        )
        if not self.isVisible():
            self.show()

    def cleanup(self):
        """程序退出时安全清理"""
        if QApplication.instance() is not None:
            self.close()


class FloatingLogger:
    """安全的日志工具包装类"""
    _instance = None

    def __init__(self):
        raise RuntimeError("请使用get_instance()获取实例")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            if QApplication.instance() is None:
                cls._init_qapplication()

            cls._instance = _FloatingLoggerImpl()
        return cls._instance

    @classmethod
    def _init_qapplication(cls):
        """安全初始化QApplication"""
        app = QApplication.instance() or QApplication(sys.argv)
        atexit.register(app.quit)


def log(message, level="info"):
    """全局日志接口"""
    logger = FloatingLogger.get_instance()
    logger.log_message(message, level)


if __name__ == '__main__':
    from PyQt5.QtCore import QTimer

    # 初始化日志系统
    logger = FloatingLogger.get_instance()


    # 异步日志测试
    def test_logging(count):
        if count < 10:
            log(f"测试消息 {count}"*50, level="info" if count % 2 else "error")
            QTimer.singleShot(500, lambda: test_logging(count + 1))


    test_logging(0)
    QApplication.instance().exec_()
