# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 5:34 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_CreateOrder.py
# @Software: PyCharm


from all_reference import *
from business.interfaces.order_service.kits.create_order_kit import CreateOrderKit

kit_obj = CreateOrderKit()

url = kit_obj.base_order_url + kit_obj.createOrder

headers = {
    "": ""
}

send = {
    "url": url,
    "headers": "",
    "json": kit_obj.get_test_data('req_json_data'),  # kit_obj.get_test_data取值防止数据被覆盖
    # "json": kit_obj.req_json_data,  # 不考虑覆盖的情况可是直接使用 kit_obj.req_json_data 直接调用
    "other": {
        "center_name": "order"
    }
}

# 多表校验，定义表名为key，方法为value
table_dict = {
    "order_001": kit_obj.assert_order1,
    "order_002": kit_obj.assert_order2,
    "order_003": kit_obj.assert_order3
}


class TestCreateOrder(BaseUnit):
    """测试创建订单"""

    # @unittest.skip("pass")
    def test_001(self):
        """基本使用"""
        # 发起请求
        resp = kit_obj.current_request(method="post", **send)

        # 获取返回值
        result = resp.json()

        # 基本断言
        kit_obj.assert_json(result, 'code', 200)
        kit_obj.assert_json(result, 'message', '操作成功')

        # 取值断言
        order_number = result.get('data').get('order_number')
        assert order_number == 123456, '订单号错误'

        # 查询数据库数据
        query_order = kit_obj.query_order(order_number)

        # 断言数据库字段
        assert query_order.get('price') == 8800.00

    @kit_obj.assert_field(table_name='order_001', table_dict=table_dict)
    @kit_obj.assert_field(table_name='order_002', table_dict=table_dict)
    @kit_obj.assert_field(table_name='order_003', table_dict=table_dict)
    def test_002(self):
        """多表校验"""
        logger.success('yyx')
        logger.error('yyx')
        kit_obj.show_result_list()


if __name__ == '__main__':
    unittest.main()
