# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 2:25 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : config.py
# @Software: PyCharm


import os
import platform
import configparser

from global_env import PROJECT_NAME


def get_config():
    """获取配置文件"""

    # conf = configparser.ConfigParser()
    conf = configparser.RawConfigParser()

    pf = platform.system()
    root_dir = os.getcwd().split(PROJECT_NAME)[0]
    linux_config = root_dir + '{}/config/server_config.ini'.format(PROJECT_NAME)
    mac_config = root_dir + '{}/config/local_config.ini'.format(PROJECT_NAME)
    windows_config = root_dir + '{}/config/local_config.ini'.format(PROJECT_NAME)
    pf_dict = {
        "Linux": {
            "config_path": linux_config,
            "msg": 'Linux配置文件:{}'.format(linux_config)
        },
        "Darwin": {
            "config_path": mac_config,
            "msg": 'Darwin->配置文件:{}'.format(mac_config)
        },
        "Windows": {
            "config_path": windows_config,
            "msg": 'Windows->配置文件:{}'.format(windows_config),
        },
    }
    config_path = pf_dict.get(pf).get('config_path')
    msg = pf_dict.get(pf).get('msg')
    print(msg)
    conf.read(config_path)
    return conf

    # # 读取配置文件里所有的Section
    # print(conf.sections())
    #
    # # 打印出test1这个section下包含key
    # print(conf.options("redis"))
    #
    # # 打印test1这个section下所有的key及对应的values
    # print(conf.items("redis"))


if __name__ == '__main__':
    conf = get_config()
