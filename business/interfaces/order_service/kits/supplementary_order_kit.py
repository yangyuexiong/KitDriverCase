# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 5:21 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : supplementary_order_kit.py
# @Software: PyCharm

from business.interfaces.order_service.kits.kits import OrderServiceCommonKit


class SupplementaryOrderKit(OrderServiceCommonKit):
    """补建订单"""

    order_add = '/order/v1/ol-order/add'

    def query_order(self, order_id):
        """查询订单表"""
        db = self.return_db(db_name='order')
        sql = """select * from `order` where id={}""".format(order_id)
        result = db.select(sql=sql, only=True)
        return result

    def func_2(self):
        """其他方法"""

    def func_3(self):
        """其他方法"""
