# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 2:49 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : base_unit.py
# @Software: PyCharm

import os
import json
import time
import warnings
import urllib3
import unittest

from types import MethodType, FunctionType


class BaseUnit(unittest.TestCase):
    start_time = 0
    end_time = 0
    total_time = 0

    class_doc = ''  # 类doc
    set_redis_key = ''  # uri
    set_redis_val = ''  # url

    is_count = False

    file_name = os.path.split(__file__)[-1].split(".")[0]

    def setUp(self):
        """
        执行前置
        :return:
        """
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        warnings.simplefilter("ignore", ResourceWarning)
        print('Start Test')
        print('>>> {} '.format(self))
        """
        self.save_doc()
        try:
            self.class_doc = self.__doc__
            print('=' * 33 + 'url param' + '=' * 33)
            url = self.class_doc.split(':')[1]
            print(url)
            self.set_redis_key = 'count_url:' + url
            self.set_redis_val = '/' + self.class_doc.split(':/')[1]

            k = self.set_redis_key
            v = self.set_redis_val
            if R.get(k):
                pass
                # print('已统计:', self.set_redis_val)
            else:
                R.set(k, v)

            print('======Test start:{}======'.format(self))
            self.start_time = time.time()
            self.is_count = True
        except BaseException as e:
            # print('跳过统计:{}'.format(str(e)))
            print('======Test start:{}======'.format(self))
        """

    def tearDown(self):
        """
        执行后置
        :return:
        """
        print('>>> End Test')
        print('>>> {} '.format(self))
        """
        if self.is_count:
            k = self.set_redis_key
            if '/' in R.get(k):
                # print('未计算:', self.set_redis_val)
                R.set(k, str(time.time() - self.start_time))
            else:
                pass
                # print('已计算')
            print('======End of test:{}======'.format(self))
        else:
            print('======End of test:{}======'.format(self))
        """

    @classmethod
    def save_doc(cls):
        """save_doc"""

        class_doc = cls.__doc__
        new_function_doc = ''

        for k, v in cls.__dict__.items():
            function_name = cls.__dict__.get(k)
            # print(kits, type(kits))
            # print(function_name)
            if isinstance(function_name, FunctionType):
                f = getattr(cls, k)
                if 'test_' in f.__name__:
                    # print(f.__name__)
                    function_doc = f.__doc__
                    # print(function_doc)
                    if function_doc:
                        new_function_doc += function_doc + '\n'
                    else:
                        pass
                else:
                    pass
                    # print('非测试func')
            else:
                pass

        set_k = 'doc_' + cls.file_name

        set_v = {
            cls.__name__: new_function_doc
        }

        # print('文件名称:', cls.file_name)
        # print('类名称:', cls.__name__)
        # print(new_function_doc)
        # print(set_k)
        # print(set_v)

        # if R.get(set_k):
        #     val = json.loads(R.get(set_k))
        #     val.update(set_v)
        #     R.set(set_k, json.dumps(val))
        # else:
        #     R.set(set_k, json.dumps(set_v))


if __name__ == '__main__':
    pass
