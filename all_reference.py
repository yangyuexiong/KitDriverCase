# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 2:25 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : all_reference.py
# @Software: PyCharm


import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from common.base_lib import *

R = BaseDataBases().get_redis()
