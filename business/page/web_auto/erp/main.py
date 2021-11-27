# -*- coding: utf-8 -*-
# @Time    : 2021/11/5 9:31 上午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : main.py
# @Software: PyCharm


from common.base_lib.base_web_driver import BaseWebDriver


class ErpWebAuto(BaseWebDriver):
    """登录"""

    def open_web(self):
        """1"""
        self.driver.get(self.url)
        print(self.driver.title)
        # sleep(3)

    def login(self, username='yangyuexiong', password='y123456'):
        """登录"""
        acc_xpath = """//*[@id="app"]/div/div[2]/form/div[2]/div/div/input"""
        pwd_xpath = """//*[@id="app"]/div/div[2]/form/div[3]/div/div/input"""
        login_button = """//*[@id="app"]/div/div[2]/form/button"""

        self.pre_wait_to_xpath(xpath=acc_xpath, t=30).send_keys(username)
        self.pre_wait_to_xpath(xpath=pwd_xpath, t=30).send_keys(password)
        self.pre_wait_to_xpath(login_button).click()

        yyx = """//*[@id="app"]/div/div[1]/div/ul/div[3]/div[2]/div/span"""
        p = self.pre_wait_to_xpath(xpath=yyx, t=30).text
        print(p)
        assert p == "杨跃雄"

    def main(self):
        """main"""
        self.start()
        self.open_web()
        self.login()
        self.end()


if __name__ == '__main__':
    erp_auto = ErpWebAuto()
    erp_auto.set_url("http://xxxxx")
    erp_auto.main()
