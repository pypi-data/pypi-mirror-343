import webview
import os
import pickle


class YkWebviewApi:
    def __init__(self) -> None:
        self.mute = False
        self.user_file = 'user.pkl'

    def printToTerm(self, msg: str, kind='info'):
        """
        打印日志到终端

        :param msg: msg中不能包含\等特殊字符串。
        :param kind: 可取值warning info success error system
        :return:
        """
        global window
        if self.mute:
            return
        if isinstance(window, webview.Window):
            cmd = f'window.printToTerm("{msg}", "{kind}")'
            window.evaluate_js(cmd, callback=None)

    def setTaskBar(self, title: str, progress: int):
        """
        设置任务栏图标和进度条

        :param title: 任务栏标题
        :param progress: 任务栏进度
        """
        global window
        if isinstance(window, webview.Window):
            cmd = f'window.setTaskBar("{title}", {progress})'
            window.evaluate_js(cmd, callback=None)

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
