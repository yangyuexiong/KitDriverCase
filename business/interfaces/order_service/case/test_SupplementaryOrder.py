# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 3:38 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_SupplementaryOrder.py
# @Software: PyCharm


from all_reference import *
from business.interfaces.order_service.kits.supplementary_order_kit import SupplementaryOrderKit

kit_obj = SupplementaryOrderKit()

url = kit_obj.base_order_url + kit_obj.order_add

headers = {
    "": ""
}

send = {
    "url": url,
    "headers": "",
    "json": "",
    "other": {
        "center_name": "order"
    }
}


class TestSupplementaryOrder(BaseUnit):
    """测试补建订单"""

    def test_001(self):
        """1"""
        print("测试补建订单")
