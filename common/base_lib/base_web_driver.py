# -*- coding: utf-8 -*-
# @Time    : 2021/11/3 6:08 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : base_web_driver.py
# @Software: PyCharm


import os
import platform
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from global_env import PROJECT_NAME


class BaseWebDriver:

    def __init__(self):
        first_path = os.getcwd().split(PROJECT_NAME)[0] + PROJECT_NAME
        if platform.system() == 'Darwin':
            self.chrome_driver = first_path + '/common/chrome_driver_mac64/chromedriver'
        elif platform.system() == 'Linux':
            self.chrome_driver = first_path + '/common/chrome_driver_linux64/chromedriver'
        elif platform.system() == 'Windows':
            self.chrome_driver = first_path + '/common/chrome_driver_win32/chromedriver'

        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless') # 无界面模式
        print('chrome driver path', self.chrome_driver)
        # self.driver = webdriver.Chrome(executable_path=self.chrome_driver, chrome_options=self.options)
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver, options=self.options)

    def start(self):
        """启动"""
        start_time = datetime.now()
        print(start_time)

    def end(self):
        """结束"""
        end_time = datetime.now()
        print(end_time)
        self.driver.quit()

    def pre_wait_to_xpath(self, xpath, t=5):
        """
        前置等待
        :param xpath: xpath路径
        :param t: 等待时间
        :return:
        """
        return WebDriverWait(self.driver, t).until(ec.presence_of_element_located((By.XPATH, xpath)))

    def ts(self, n):
        """隐式等待"""
        self.driver.implicitly_wait(n)

    def test(self):
        self.start()
        self.driver.get('https://www.baidu.com')
        print(self.driver.title)
        time.sleep(3)
        self.end()


if __name__ == '__main__':
    bwd = BaseWebDriver()
    bwd.test()
