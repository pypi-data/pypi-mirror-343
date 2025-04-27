import json
import os.path
import re
import subprocess
import sys
from time import sleep

from ddddocr import DdddOcr
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from simonPackage.rw import color_print


class Web:
    """
    普通隐身浏览器
    """

    def __init__(self, visible=True):
        super(Web, self).__init__()
        self.visible = visible
        self.account = ''
        # 1初始化浏览器对象
        opt = Options()

        # 隐身防检测
        opt.add_argument("disable-blink-features=AutomationControlled")
        opt.add_experimental_option('useAutomationExtension', False)
        opt.add_experimental_option("excludeSwitches", ['enable-automation'])
        opt.add_argument('--start-maximize')
        opt.add_argument('--disable-dev-shm-usage')
        opt.add_argument('--no-sandbox')
        opt.add_argument('--disable-infobars')

        # 无头浏览器设置选项
        if not self.visible:
            opt.add_argument('--headless')
            opt.add_argument('--disable-gpu')
        self.driver = Chrome(options=opt)
        self.driver.implicitly_wait(10)

    @staticmethod
    def login(login_function):
        """为不同的登录方式提供统一的函数入口"""
        login_function()

    def saveCookies(self, filename='cookies.json'):
        cookies_list = self.driver.get_cookies()

        # 指定了要将该数字列表存储到哪个⽂件中
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(cookies_list, f)

    def loadCookies(self, filename='cookies.json'):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                cookies_list = json.load(f)
            self.setCookies(cookies_list)
        except FileNotFoundError:
            pass

    @staticmethod
    def autoMaxCookieExpiry(filename='cookies.json'):
        """自动将cookies中所有过期时间推后至其中最长时限"""
        with open(filename, 'r', encoding='utf-8') as f:
            # cookies_list = json.load(f)
            cookies_str = f.read()
        # 10 digits time stamp
        pattern = r'"expiry": (1\d{9})'
        # 非原地操作
        cookies_str, _ = re.subn(pattern, max(re.findall(pattern, cookies_str)), cookies_str)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(cookies_str)

    def setCookies(self, cookies_list):
        self.driver.delete_all_cookies()
        for cookie in cookies_list:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

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

    def switchLast(self):
        """
        快捷转向新打开的窗口
        """
        self.switch_to.window(self.window_handles[-1])

    def findXpath(self, xpath):
        return self.driver.find_element(by=By.XPATH, value=xpath)


class WebDebug:
    """
    启动本地已经打开的浏览器作为控制对象
    """

    def __init__(self, visible=True):
        self.visible = visible
        cmd = 'chromium --remote-debugging-port=9999 --start-maximized' if sys.platform == 'linux' else 'chrome.exe --remote-debugging-port=9999 --start-maximized'
        subprocess.Popen(cmd, shell=True)

        cmd = 'google-chrome --remote-debugging-port=9999 --start-maximized' if sys.platform == 'linux' else 'chrome.exe --remote-debugging-port=9999 --start-maximized'
        print(subprocess.Popen(cmd, shell=True))
        sleep(3)

        opt = Options()
        opt.add_experimental_option('debuggerAddress', '127.0.0.1:9999')
        # 防检测
        opt.add_argument("disable-blink-features=AutomationControlled")
        # opt.add_experimental_option('useAutomationExtension', False)
        # opt.add_experimental_option("excludeSwitches", ['enable-automation'])
        opt.add_argument('--start-maximize')
        opt.add_argument('--disable-dev-shm-usage')
        opt.add_argument('--no-sandbox')
        opt.add_argument('--disable-infobars')
        self.driver = Chrome(options=opt)  # service=service,
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webself.driver", {get:()=>undefined})'})
        self.driver.implicitly_wait(10)

        # self.driver.get('https://www.xuexi.cn')
        self.driver.get('https://pc.xuexi.cn/points/my-points.html')
        self.driver.execute_script('window.scrollBy(0, 1000)')
        # 扫码登录
        sleep(60)

    def setCookies(self, cookies_list):
        self.driver.delete_all_cookies()
        for cookie in cookies_list:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    def findXpath(self, xpath):
        return self.driver.find_element(by=By.XPATH, value=xpath)

    def saveCookies(self):
        cookies_list = self.driver.get_cookies()
        filename = 'cookies.json'
        # 指定了要将该数字列表存储到哪个⽂件中
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(cookies_list, f)


class WebGanbu(Chrome):
    def __init__(self, login_url='http://www.hebgb.gov.cn/index.html', account='130532198407262015', password='240784',
                 class_id=None, visible=False, is_specialization=True, speed_play=True, night_study=False):
        """
        :param login_url: web page of login
        :param account: 18 digits of id card
        :param password: password
        :param class_id: class_id if None will study all the available classes
        :param visible: whether to show the browser
        :param is_specialization: special class or random class
        """
        super().__init__()
        self.all_class_courses = []
        self.class_ids = []
        self.courses_done = []
        self.login_url = login_url
        self.account = account
        self.password = password
        self.class_id = class_id
        self.is_specialization = is_specialization
        self.speed_play = speed_play
        self.night_study = night_study
        # 1初始化浏览器对象
        opt = Options()
        # # 隐身防检测

        opt.add_argument("disable-blink-features=AutomationControlled")
        opt.add_experimental_option('useAutomationExtension', False)
        opt.add_experimental_option("excludeSwitches", ['enable-automation'])
        opt.add_argument('--start-maximize')
        opt.add_argument('--disable-dev-shm-usage')
        opt.add_argument('--no-sandbox')
        opt.add_argument('--disable-infobars')

        """无头浏览器设置选项"""
        if not visible:
            opt.add_argument('--headless')
            opt.add_argument('--disable-gpu')
        self.driver = Chrome(options=opt)
        self.driver.implicitly_wait(10)
        self.total_courses = 0

    def login(self, login_url, account, password, account_xpath, password_xpath, login_btn_xpath=None):
        # 打开登录界面
        self.get(self.login_url)
        self.switch_to.window(self.driver.window_handles[-1])
        # 执行登录操作
        """输入用户名和密码，点击登录"""
        self.find_element(by=By.XPATH, value=account_xpath).send_keys(self.account)
        self.find_element(by=By.XPATH, value=password_xpath).send_keys(self.password, Keys.ENTER)
        if login_btn_xpath:
            self.find_element(by=By.XPATH, value=login_btn_xpath).click()
        color_print('登录成功！'.center(15, '*'), mode='default', font_color='green')
        print('-' * 100)

    def switchLast(self):
        self.switch_to.window(self.window_handles[-1])

    def verify(self, verify_url, verifycode_xpath, verify_enter_xpath):
        self.get(verify_url)
        self.switchLast()
        verifycode_png = self.find_element(by=By.XPATH, value=verifycode_xpath).screenshot_as_png
        ocr = DdddOcr(show_ad=False)
        verify_code = ocr.classification(verifycode_png)
        # print(verify_code)
        self.find_element(by=By.XPATH, value=verify_enter_xpath).send_keys(verify_code, Keys.ENTER)

    def verifyTillSucceed(self, verify_url, verifycode_xpath, verify_enter_xpath):
        verifycode_el = self.find_element(by=By.XPATH, value=verifycode_xpath)
        while verifycode_el:
            self.verify(verify_url, verifycode_xpath, verify_enter_xpath)
            verifycode_el = self.find_element(by=By.XPATH, value=verifycode_xpath)
        else:
            print('login success')

    def writeLog(self, info):
        # 学习完后添加到日志中
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


if __name__ == '__main__':
    web = Web(visible=True)
    # verifycode_xpath = '//*[@id="kaptcha"]'
    # verifyenter_xpath = '/html/body/div[1]/div/div/form/div[3]/input'
    # verify_url = 'http://www.hbrdlz.com/'
    # web.verify(verify_url, verifycode_xpath, verifyenter_xpath)
