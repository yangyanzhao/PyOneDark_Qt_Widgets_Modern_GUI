import os
import atexit

import ctypes
import psutil
import win32gui
import win32process


class FileLock:
    lockfile = "app.lock"

    def __init__(self, lockfile=lockfile):
        self.lockfile = lockfile
        self.acquire()

    def acquire(self):
        if os.path.exists(self.lockfile):
            return False
        with open(self.lockfile, 'w') as f:
            f.write(str(os.getpid()))
        atexit.register(self.release)
        return True

    def release(self):
        os.remove(self.lockfile)

    @staticmethod
    def get_pid():
        if os.path.exists(FileLock.lockfile):
            with open(FileLock.lockfile, 'r') as f:
                pid = int(f.read().strip())
            return pid
        else:
            return None

    @staticmethod
    def find_and_activate_window(window_title):
        """
        根据窗口名称激活窗口
        :param window_title:
        :return:
        """
        hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 5)  # SW_SHOW
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            return True
        return False

    @staticmethod
    def is_pid_running(pid):
        """
        检查给定的 PID 是否正在运行。

        :param pid: 要检查的进程 ID
        :return: 如果 PID 正在运行，返回 True；否则返回 False
        """
        print(f"PID:{pid}")
        if pid is None:
            return False
        try:
            # 尝试获取进程信息
            process = psutil.Process(pid)
            # 如果进程存在，process 对象会被创建
            return True
        except psutil.NoSuchProcess:
            # 如果进程不存在，会抛出 NoSuchProcess 异常
            return False
