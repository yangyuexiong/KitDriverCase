# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 3:38 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_SupplementaryOrder.py
# @Software: PyCharm


from all_reference import unittest, BaseUnit, env
from common.base_lib.base_kit import BaseKit

kit_obj = BaseKit()


class TestDemo001(BaseUnit):
    """TestDemo001"""

    def test_001(self):
        """1"""
        print(env)


if __name__ == '__main__':
    unittest.main()
