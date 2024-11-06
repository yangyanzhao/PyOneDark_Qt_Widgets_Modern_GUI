import os


class StartupManager:
    """
    开机启动管理器
    """

    def __init__(self, exe_name, bat_name="startup"):
        """
        初始化
        :param exe_name: 程序名称
        :param bat_name: 脚本名称
        """
        super().__init__()
        self.bat_name = bat_name
        self.exe_name = exe_name

    def check_startup_status(self):
        bat_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup',
                                f'{self.bat_name}.bat')
        if os.path.exists(bat_path):
            return True
        else:
            return False

    def add_to_startup(self):
        file_path = os.path.join(os.getcwd(), f"{self.exe_name}.exe")
        bat_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup',
                                f'{self.bat_name}.bat')
        print(bat_path)
        with open(bat_path, "w+") as bat_file:
            bat_file.write(r'start "" "%s"' % file_path)

    def remove_from_startup(self):
        bat_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup',
                                f'{self.bat_name}.bat')
        print(bat_path)
        if os.path.exists(bat_path):
            os.remove(bat_path)


if __name__ == '__main__':
    manager = StartupManager("main")
    status = manager.check_startup_status()
    print(status)
    manager.remove_from_startup()
    # manager.add_to_startup()
