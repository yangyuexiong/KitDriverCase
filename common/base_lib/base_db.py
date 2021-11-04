# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 3:17 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : base_db.py
# @Software: PyCharm

import json
from datetime import datetime

import decimal
import pymysql
import redis
from elasticsearch import Elasticsearch

from config.config import get_config


class MyPyMysql:
    def __init__(self, host=None, port=None, user=None, password=None, db=None, debug=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.debug = debug

    def db_obj(self):
        """
        返回db对象
        :return:
        """
        try:
            database_obj = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db)
            return database_obj
        except BaseException as e:
            return '连接数据库参数异常{}'.format(str(e) if self.debug else '')

    def create_data(self, sql=None):
        """
        新增
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                print(sql)
                cur.execute(sql)
                db.commit()
                return 'create success'
        except BaseException as e:
            cur.rollback()
            return 'create:出现错误:{}'.format(str(e) if self.debug else '')

    def read_data(self, sql=None):
        """
        查询(废弃,保留实现思想)(使用: MyPyMysql.select 代替之)
        :param sql:
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                cur.execute(sql)  # 执行sql语句
                # sql = "select * from gambler where id='YfpgoLZtEGPfMXUvFPffCi'"

                '''
                获取表结构,并且取出字段,生成列表
                '''
                '''获取字段列表'''
                # print(cur.description)
                key_list = [i[0] for i in cur.description]
                # print(key_list)

                '''
                把查询结果集组装成列表
                '''
                results = cur.fetchall()
                # print(results)
                data_list = [i for i in results]
                # print(data_list)

                data_dict = []
                for field in cur.description:
                    data_dict.append(field[0])
                # print(data_dict)
                # print(len(data_dict))

                '''
                将字段与每一条查询数据合并成键值对,并且组装成新的列表
                new_list = []
                for i in data_list:
                    print(list(i))
                    new_list.append(dict(zip(key_list, list(i))))
                '''
                new_list = [dict(zip(key_list, list(i))) for i in data_list]
                # print(new_list)
                return new_list
        except BaseException as e:
            return 'read:出现错误:{}'.format(str(e) if self.debug else '')

    def update_data(self, sql=None):
        """
        更新
        :param sql:
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                cur.execute(sql)
                db.commit()
                return 'update success'
        except BaseException as e:
            cur.rollback()
            return 'update:出现错误:{}'.format(str(e) if self.debug else '')

    def del_data(self, sql=None):
        """
        删除
        :param sql:
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                cur.execute(sql)
                db.commit()
                return 'del success'
        except BaseException as e:
            cur.rollback()
            return 'del:出现错误:{}'.format(str(e) if self.debug else '')

    def select(self, sql=None, only=None, size=None):
        """
        查询
        :param sql:
        :param only:
        :param size:
        :return:
        """

        def __func(r):
            if isinstance(r, list):
                new_list = []
                for i in r:
                    new_r = {}
                    for k, v in i.items():
                        if isinstance(v, decimal.Decimal):
                            # v = float(decimal.Decimal(v).quantize(decimal.Decimal("0.0")))
                            v = str(v)
                            v = float(v)
                            new_r[k] = v
                        elif isinstance(v, str):
                            try:
                                new_v = json.loads(v)
                                if isinstance(new_v, list) or isinstance(new_v, dict):
                                    new_r[k] = new_v
                                else:
                                    new_r[k] = v
                            except BaseException as e:
                                new_r[k] = v
                                # print(k, v, type(v))
                                # print("select.__func 异常:{}".format(str(e) if self.debug else ''))
                        elif isinstance(v, datetime):
                            new_r[k] = str(v)
                        else:
                            new_r[k] = v
                    new_list.append(new_r)
                return new_list
            elif isinstance(r, dict):
                new_r = {}
                for k, v in r.items():
                    if isinstance(v, decimal.Decimal):
                        # v = float(decimal.Decimal(v).quantize(decimal.Decimal("0.0")))
                        v = str(v)
                        v = float(v)
                        new_r[k] = v
                    elif isinstance(v, str):
                        try:
                            new_v = json.loads(v)
                            if isinstance(new_v, list) or isinstance(new_v, dict):
                                new_r[k] = new_v
                            else:
                                new_r[k] = v
                        except BaseException as e:
                            new_r[k] = v
                    elif isinstance(v, datetime):
                        new_r[k] = str(v)
                    else:
                        new_r[k] = v
                return new_r
            else:
                pass

        try:
            db = self.db_obj()
            with db.cursor(pymysql.cursors.DictCursor) as cur:
                cur.execute(sql)  # 执行sql语句
                if only and not size:  # 唯一结果返回 json/dict
                    rs = cur.fetchone()
                    result = __func(rs)
                    return result
                if size and not only:  # 按照需要的长度返回
                    rs = cur.fetchmany(size)
                    result = __func(rs)
                    return result
                else:  # 返回结果集返回 list
                    rs = cur.fetchall()
                    result = __func(rs)
                    return result
        except BaseException as e:
            return 'select:出现错误:{}'.format(str(e) if self.debug else '')


class DbConnectionConfig:
    """数据连接配置"""
    conf = get_config()
    redis_obj = {
        'host': conf.get('redis', 'REDIS_HOST'),
        'port': conf.get('redis', 'REDIS_PORT'),
        'password': conf.get('redis', 'REDIS_PWD'),
        'decode_responses': conf.getboolean('redis', 'DECODE_RESPONSES'),
        'db': conf.getint('redis', 'REDIS_DB')
    }
    POOL = redis.ConnectionPool(**redis_obj)
    R = redis.Redis(connection_pool=POOL)

    uat_db_connection = {
        'host': conf.get('mysql', 'UAT_HOST'),
        'user': conf.get('mysql', 'UAT_USER'),
        'password': conf.get('mysql', 'UAT_PWD'),
        'db': conf.get('mysql', 'UAT_DB'),
        'port': conf.getint('mysql', 'UAT_PORT'),
    }

    pre_db_connection = {}

    uat_es_connection = {
        'url': conf.get('es', 'ES_URL'),
        'user': conf.get('es', 'ES_USER'),
        'pwd': conf.get('es', 'ES_PWD')
    }


class BaseDataBases(DbConnectionConfig):
    """db"""

    @classmethod
    def return_default_db(cls, env):
        """
        默认库
        """
        if env == 'uat':
            return MyPyMysql(**cls.uat_db_connection)

        if env == 'pre':
            return MyPyMysql(**cls.pre_db_connection)
        else:
            msg = 'return_db -> 变量:{} 错误'.format(env)
            print(msg)
            return False

    def get_env(self, default_env="uat"):
        """
        获取环境
        :return:
        """
        try:
            return self.get_redis().get('env')

        except:
            return default_env

    def get_redis(self):
        """
        获取Redis
        :return:
        """
        try:
            return self.R

        except BaseException as e:
            print('return_redis -> redis err -> {}'.format(str(e)))
            return False

    def return_db(self, db_name=None):
        """
        获取数据库
        :return:
        """
        if db_name and self.get_env() == 'uat':
            try:
                before_uat_db_connection = self.uat_db_connection.copy()
                before_uat_db_connection['db'] = db_name
                return MyPyMysql(**before_uat_db_connection)

            except BaseException as e:
                print('return_db -> 变量:{}'.format(self.get_env()))
                print('UAT:未找到该数据库名称:{}'.format(db_name))
                print(str(e))
                return False

        if db_name and self.get_env() == 'pre':
            try:

                before_pre_db_connection = self.pre_db_connection.copy()
                before_pre_db_connection['db'] = db_name
                return MyPyMysql(**before_pre_db_connection)

            except BaseException as e:
                print('return_db -> 变量:{}'.format(self.get_env()))
                print('PRE:未找到该数据库名称:{}'.format(db_name))
                print(str(e))
                return False
        else:
            return self.return_default_db(self.get_env())

    def return_es(self, env='uat'):
        """获取es"""
        if env == 'uat':
            es = Elasticsearch(
                [self.uat_es_connection.get('url')],
                http_auth=(self.uat_es_connection.get('user'), self.uat_es_connection.get('pwd'))  # 认证信息
            )
        elif env == 'prod':
            prod_es_connection = {
                'url': self.conf.get('es_prod', 'ES_URL'),
                'user': self.conf.get('es_prod', 'ES_USER'),
                'pwd': self.conf.get('es_prod', 'ES_PWD')
            }
            es = Elasticsearch(
                [prod_es_connection.get('url')],
                http_auth=(prod_es_connection.get('user'), prod_es_connection.get('pwd'))  # 认证信息
            )
        else:
            es = None
            print('es 不存在')
        return es
