import webview
import os
import pickle


class YkWebviewApi:
    def __init__(self) -> None:
        self.mute = False
        self.user_file = 'user.pkl'
        self.window = None

    def printToTerm(self, msg: str, kind='info'):
        """
        打印日志到终端

        :param msg: msg中不能包含\等特殊字符串。
        :param kind: 可取值warning info success error system
        :return:
        """
        if self.mute:
            return
        if isinstance(self.window, webview.Window):
            cmd = f'window.printToTerm("{msg}", "{kind}")'
            self.window.evaluate_js(cmd, callback=None)

    def setTaskBar(self, title: str, progress: int):
        """
        设置任务栏图标和进度条

        :param title: 任务栏标题
        :param progress: 任务栏进度
        """
        if isinstance(self.window, webview.Window):
            cmd = f'window.setTaskBar("{title}", {progress})'
            self.window.evaluate_js(cmd, callback=None)

    def saveLoginInfo(self, userInfo: dict):
        """
        保存登录信息到本地user.pkl文件

        :param userInfo: 用户信息字典，包含username和password
        """
        try:
            with open(self.user_file, 'wb') as f:
                pickle.dump(userInfo, f)
            return True
        except Exception as e:
            print(f"保存登录信息失败: {e}")
            return False

    def getLoginInfo(self):
        """
        获取登录信息，读取本地文件user.pkl保存的username和password

        :return: 用户名和密码
        """
        if not os.path.exists(self.user_file):
            return None

        try:
            with open(self.user_file, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"读取登录信息失败: {e}")
            return None

    def toggle_fullscreen(self):
        """
        全屏
        """
        if isinstance(self.window, webview.Window):
            self.window.toggle_fullscreen()
            from webview import localization

    def start(self, window, ssl=True, debug=True, localization=None):
        """
        启动webview窗口
        """
        if localization is None:
            localization = {
                'global.quitConfirmation': u'确定关闭?',
                'global.ok': '确定',
                'global.quit': '退出',
                'global.cancel': '取消',
                'global.saveFile': '保存文件',
                'windows.fileFilter.allFiles': '所有文件',
                'windows.fileFilter.otherFiles': '其他文件类型',
                'linux.openFile': '打开文件',
                'linux.openFiles': '打开文件',
                'linux.openFolder': '打开文件夹',
            }

        self.window = window

        # 启动窗口
        # webview.start(localization=chinese, http_server=True, debug=True)
        # webview.start(custom_logic, window)  # 传入的函数会被立即执行
        webview.start(localization=localization, ssl=ssl,
                      debug=debug)  # 该语句会阻塞，直到程序关闭后才会继续执行后续代码
