# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 4:50 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : kits.py
# @Software: PyCharm


from all_reference import *


class OrderServiceCommonKit(BaseKit, BaseDataBases):
    """订单服务通用套件"""

    env = "uat"

    order_url_dict = {
        'def': 'https://uat-order.xxxxxx.cn',
        'uat': 'https://uat-order.xxxxxx.cn',
        'pre': 'https://pre-order.xxxxxx.cn',
        'prod': 'https://order.xxxxxx.cn'
    }
    base_order_url = order_url_dict.get(env, 'def')

    def func_1(self):
        """1"""

    def func_2(self):
        """1"""

    def func_3(self):
        """1"""


class SubmoduleKit(OrderServiceCommonKit):
    """子模块套件"""

    addOrder = '/trade_order/v1/saleOrder/addOrder'
