# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 5:24 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : create_order_kit.py
# @Software: PyCharm

from all_reference import env
from business.interfaces.order_service.kits.kits import OrderServiceCommonKit


class CreateOrderKit(OrderServiceCommonKit):
    """创建订单"""

    env = env
    createOrder = '/order/v1/ol-order/createOrder'

    req_json_data = {
        "userId": 123456,
        "price": 8800.00,
        "payType": 99
    }

    def query_order(self, order_id):
        """查询订单表"""
        db = self.return_db(db_name='order')
        sql = """select * from `order` where id={}""".format(order_id)
        result = db.select(sql=sql, only=True)
        return result

    def assert_order(self, *args, **kwargs):
        """校验order表字段"""

    def assert_order1(self):
        """assert_order1"""

    def assert_order2(self):
        """assert_order2"""

    def assert_order3(self):
        """assert_order3"""
