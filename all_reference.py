# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 2:25 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : all_reference.py
# @Software: PyCharm

import os
import unittest
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from loguru import logger

from common.base_lib.base_unit import BaseUnit

env = os.environ.get('env', 'uat')
debug = os.environ.get('DEBUG', True)
print('env:{}'.format(env))
print('debug:{}'.format(debug))
