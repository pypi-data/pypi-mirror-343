import json
import os.path
import re
import sys
from time import sleep

from ddddocr import DdddOcr
from DrissionPage import WebPage, ChromiumOptions
from DrissionPage.common import By
from DrissionPage.common import Keys
from ..rw import color_print


class WebDP:
    """
    普通隐身浏览器
    """

    def __init__(self, visible=True):
        super(WebDP, self).__init__()
        self.visible = visible
        self.account = ''
        # 1初始化浏览器对象
        """无头浏览器设置选项"""
        self.co = ChromiumOptions().headless(not visible).auto_port(True).mute()
        if sys.platform == 'linux':
            _browser360_path = '/opt/apps/com.360.browser-stable/files/com.360.browser-stable'
            if os.path.exists(_browser360_path):
                self.co.set_browser_path(_browser360_path)

        # 1初始化浏览器对象

            self.driver = WebPage(chromium_options=self.co)
        else:
            self.driver = WebPage(chromium_options=self.co)
            sleep(30)

    @staticmethod
    def login(login_function):
        """为不同的登录方式提供统一的函数入口"""
        login_function()

    def saveCookies(self, cookie_path):

        cookies_list = self.driver.cookies()

        # 指定了要将该数字列表存储到哪个⽂件中
        with open(cookie_path, 'w', encoding='utf-8') as f:
            json.dump(cookies_list, f)

    def setCookies(self, cookies_list):
        self.driver.set.cookies.clear()
        for cookie in cookies_list:
            self.driver.set.cookies(cookie)
        self.driver.refresh()

    def loadCookies(self, cookie_path):
        try:
            with open(cookie_path, 'r', encoding='utf-8') as f:
                cookies_list = json.load(f)
            self.setCookies(cookies_list)
        except FileNotFoundError:
            os.makedirs('res', exist_ok=True)

    @staticmethod
    def autoMaxCookieExpiry(cookie_path):
        """自动将cookies中所有过期时间推后至其中最长时限"""
        with open(cookie_path, 'r', encoding='utf-8') as f:
            # cookies_list = json.load(f)
            cookies_str = f.read()
        # 10 digits time stamp
        pattern = r'"expiry": (1\d{9})'
        # 非原地操作
        expire_cookies = re.findall(pattern, cookies_str)
        if expire_cookies:
            cookies_str, _ = re.subn(pattern, '"expiry": ' + max(re.findall(pattern, cookies_str)), cookies_str)
        with open(cookie_path, 'w', encoding='utf-8') as f:
            f.write(cookies_str)


    def writeLog(self, info):
        # 学习完后添加到日志中
        if not os.path.exists('res'):
            os.mkdir('res')
        with open(f'res/{self.account}log.txt', 'a') as f:
            f.write(info)

    def readLog(self):
        # 学习前查找日志
        try:
            with open(f'res/{self.account}log.txt', 'r') as f:
                log = f.read()
        except:
            log = ''
        self.courses_done = re.findall(r'http:.*', log)

    def switchLast(self, sleep_sec=1):
        """快捷转向新打开的窗口"""
        self.driver.get_tab(0)
        sleep(sleep_sec)

    def findXpath(self, xpath):
        return self.driver.ele(f'x:{xpath}')



if __name__ == '__main__':
    web = WebDP(visible=True)
    
