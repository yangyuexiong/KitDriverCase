# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 2:48 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : base_kit.py
# @Software: PyCharm

import copy
import json
from functools import wraps
from types import MethodType, FunctionType

import requests
from all_reference import env


class BaseKit:
    """测试工具包基类"""

    env = env
    assert_switch = False
    test_data = {
        "key": "value"
    }
    current_test_data = {}
    current_url = {}
    current_headers = {}
    current_resp_json = {}
    to_assert_json_data = {}
    to_assert_resp_json = {}
    resp_json_data = {}
    table_dict = {}
    err_result_list = []

    @classmethod
    def data_init(cls):
        """数据初始化"""

    @classmethod
    def show_log(cls, url=None, headers_param=None, json_param=None, json_response=None, json_response_headers=None):
        """
        打印请求日志
        :param url: URL
        :param headers_param: 请求头
        :param json_param: 请求体
        :param json_response: 返回值
        :param json_response_headers: 返回头
        :return:
        """
        try:
            print('=' * 33 + ' url ' + '=' * 33)
            print(url)

            print('=' * 33 + ' headers param ' + '=' * 33)
            cls.json_format(headers_param)

            print('=' * 33 + ' json or param ' + '=' * 33)
            cls.json_format(json_param)

            print('=' * 33 + ' response_headers ' + '=' * 33)
            cls.json_format(json_response_headers)

            print('=' * 33 + ' response ' + '=' * 33)
            cls.json_format(json_response)

            print('=' * 33 + ' end show log ' + '=' * 33)
        except BaseException as e:
            print('show_log error {}'.format(str(e)))

    @classmethod
    def show_doc(cls, func_doc):
        """
        打印函数名称
        :param func_doc: 函数 __doc__
        :return:
        """
        print('=' * 33 + func_doc + '=' * 33)

    @classmethod
    def get_test_data(cls, data):
        """防止类数据共享问题"""
        if hasattr(cls, data):
            if isinstance(getattr(cls, data), int):
                cls.current_test_data = getattr(cls, data)
                return cls.current_test_data
            else:
                # new_data = getattr(cls, data).copy()
                new_data = copy.deepcopy(getattr(cls, data))
                cls.current_test_data = new_data.get(cls.env) if new_data.get(cls.env) else new_data
                return cls.current_test_data

        else:
            return None

    @classmethod
    def current_request(cls, method=None, is_enc=None, **kwargs):
        """
        构造请求
        :param method: 请求方式
        :param is_enc: 是否加密
        :param kwargs: 定制化部分(请求体以及扩展参数)
        :return:
        """

        d = kwargs.get('json', kwargs.get('data', kwargs.get('params')))
        if is_enc:
            pass
            # center_name = kwargs.get('other', {}).get('center_name', None)
            # kwargs.get('headers').update({"sign": cls.create_sign(d, center_name=center_name)})
        else:
            pass

        if kwargs.get('other'):
            del kwargs['other']
        else:
            pass

        cls.current_url = kwargs.get('url')
        cls.current_headers = kwargs.get('headers')

        if hasattr(requests, method):
            response = getattr(requests, method)(**kwargs, verify=False)
            cls.current_resp_json = response.json()
            cls.show_log(cls.current_url, cls.current_headers, d, cls.current_resp_json, response.headers)
        else:
            response = {
                "error": "requests 没有 {} 方法".format(method)
            }
            cls.current_resp_json = response
            cls.show_log(cls.current_url, cls.current_headers, d, cls.current_resp_json, {})
        return response

    @classmethod
    def assert_response(cls, resp, *args, **kwargs):
        """检查:response"""
        print(resp)
        print(args)
        print(kwargs)

    @classmethod
    def assert_db(cls):
        """检查:db"""

    @classmethod
    def assert_json(cls, json_obj, key, val):
        """
        断言json
        :param json_obj:json对象
        :param key: 键
        :param val: 值
        :return:
        """
        assert json_obj[key] == val

    @classmethod
    def null_check_list(cls, parameter):
        """
        组装空值校验参数list
        :param parameter:
        :return:
        """

        index_list = []
        json_list = []

        def null_check(index, json_param):
            for i, kv in enumerate(json_param):
                if i == index:
                    json_param[kv] = ''
                    new_json_param = json_param
                    # print(new_json_param)
                    return new_json_param
                else:
                    pass

        if isinstance(parameter, dict):
            result_list = [parameter for i in range(len(parameter))]
            # print(result_list)
            for index, value in enumerate(result_list):
                # print(index, value)
                if index in index_list:
                    pass
                else:
                    index_list.append(index)
                    json_list.append(null_check(index, value.copy()))
        else:
            pass
        return json_list

    @classmethod
    def json_format(cls, d):
        """json格式打印"""
        try:
            print(json.dumps(d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
        except BaseException as e:
            # print('json格式打印异常:{}\n'.format(str(e)))
            print(d)

    @classmethod
    def get_assert_msg(cls, msg):
        """
        获取检验的明细list
        """
        new_list = msg.split('\n')
        new_list = list(filter(None, [i.lstrip() for i in list(filter(None, new_list))]))
        # print(new_list)
        return new_list

    @classmethod
    def yyx_skip(cls, sw=False, msg='pass', func=None, **kwargs):
        """
        :sw:是否跳过
        :msg:跳过描述
        :func:函数
        :kwargs:函数的参数
        """
        print('yyx_skip', sw)
        if sw and (isinstance(func, FunctionType) or isinstance(func, MethodType)):
            return func(**kwargs)
        else:
            print(msg)
            assert 1 == 0, msg

    @classmethod
    def assert_field(cls, table_name, table_dict):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kw):
                # print('%s %s():' % (table_name, func.__name__))
                try:
                    table_dict.get(table_name)()
                except BaseException as e:
                    err_msg = '{}:{}'.format(table_name, str(e))
                    cls.err_result_list.append(err_msg)
                return func(*args, **kw)

            return wrapper

        return decorator

    def show_result_list(self):
        """
        字段断言输出,在调用 BaseKit.assert_field 后调用
        """
        if self.err_result_list:
            err_detail = '\n'.join(self.err_result_list)
            self.err_result_list.clear()
            assert False, '{}'.format(err_detail)
