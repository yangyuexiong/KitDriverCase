# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 2:19 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : run.py
# @Software: PyCharm


import os
import sys
import json
import platform
import argparse
import unittest
from ast import literal_eval

from common.base_lib.base_db import BaseDataBases
from common.base_lib.JsonTestRunner import JsonTestRunner
from common.base_lib.base_tools import BaseTools, SendEmail, gen_branch

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])

R = BaseDataBases.get_redis()


def gen_shell():
    """生成python shell命令"""
    parser = argparse.ArgumentParser(description="作者:杨跃雄")
    parser.add_argument('--title', type=str, default='自动化测试报告', help='报告标题:如-平台发展自动化测试报告')
    parser.add_argument('--desc', type=str, default='描述', help='报告描述:如-交易域')
    parser.add_argument('--tester', type=str, default='测试人员:yyx', help='测试人员')
    parser.add_argument('--env', type=str, default='uat', help='运行环境(uat,pre,prod)')
    parser.add_argument('--cf', type=str, default='*', help='默认全部,否则:指定路径用于配置jenkins区分job')
    parser.add_argument('--fp', type=str, default='test*.py', help='默认test开头全部,否则:指定某个文件')
    parser.add_argument('--is_mail', type=int, default=0, help='是否发送邮件(1:是,0:否)默认为0')
    parser.add_argument('--is_print', type=int, default=0, help='打印json格式的测试结果(1:是,0:否)默认为0')
    parser.add_argument('--is_xm', type=int, default=0, help='生成XMind(1:是,0:否)默认为0')
    parser.add_argument('--is_debug', type=int, default=0, help='是否debug模式(1:是,0:否)默认为0')
    parser.add_argument('--is_dd_push', type=int, default=1, help='是否钉钉推送(1:是,0:否)默认为1')
    args = parser.parse_args()
    env = args.env if args.env in ['uat', 'pre', 'prod'] else 'uat'
    cf = os.getcwd() if args.cf == "*" else args.cf
    fp = args.fp
    is_mail = args.is_mail
    is_print = args.is_print
    title = args.title
    description = args.desc
    tester = args.tester
    is_xm = args.is_xm
    is_debug = args.is_debug
    is_dd_push = args.is_dd_push

    is_dd_push = bool(is_dd_push)
    is_debug = bool(is_debug)
    is_print = bool(is_print)
    is_mail = bool(is_mail)
    is_xm = bool(is_xm)

    main_init = {
        'title': title,
        'description': description,
        'tester': tester,
        'env': env,
        'path': cf,
        'file_prefix': fp,
        'is_debug': is_debug,
        'is_print': is_print,
        'is_mail': is_mail,
        'is_xm': is_xm,
        'is_dd_push': is_dd_push
    }
    print('====================')
    print('执行环境:{}'.format(env))
    print('绝对路径:{}'.format(cf))
    print('用例文件:{}'.format(fp))
    print('是否调试:{}'.format(is_debug))
    print('是否打印:{}'.format(is_print))
    print('邮件发送:{}'.format(is_mail))
    print('XMind:{}'.format(is_xm))
    print('钉钉推送:{}'.format(is_dd_push))
    print(main_init)
    print(
        'Command:python3 run.py --title {} --desc {} --tester {} --is_print {} --env {} --cf {} --mail {} --is_dd_push {}'.format(
            title, description, tester, is_print, env, cf, is_mail, is_dd_push
        ))
    print('====================')
    return main_init


class MainTest:
    """
    测试执行
    - env -- 执行环境
    - path -- 执行绝对路径
    - file_prefix -- 是否指定测试文件,否则默认 test*.py
    - is_mail -- 是否发送邮件
    - title -- 报告标题
    - description -- 报告描述
    - tester -- 测试人员名称
    - is_print -- 打印json格式的测试结果
    - is_xm -- 生成XMind
    - is_debug -- 调试模式
    - is_dd_push -- 钉钉推送
    """

    def __init__(self, env, path, file_prefix=None, is_mail=False, title=None, description=None, tester=None,
                 is_print=None, is_xm=None, is_debug=None, is_dd_push=True):
        self.pf = platform.system()
        self.env = env
        self.path = path
        self.report_dir = os.getcwd() + '/reports'
        self.xm_dir = os.getcwd() + '/xminds'
        self.file_prefix = file_prefix if file_prefix else 'test*.py'
        self.d = {
            'report_dir': self.report_dir,
            'test_dir': self.path,
            'file_prefix': self.file_prefix
        }
        self.report_path = None
        self.report_name = None
        self.discover = None
        self.is_debug = is_debug
        self.is_print = is_print
        self.is_mail = is_mail
        self.is_xm = is_xm
        self.title = title if title else '平台发展自动化测试报告'
        self.description = description if description else '交易域'
        self.tester = tester if tester else '杨跃雄'
        self.jtr_dict = {
            'title': self.title,
            'description': self.description,
            'tester': self.tester
        }
        self.json_test_result = {}
        self.xmind_dict = [
            {
                "redis_key": "XMind_SupplementaryOrder",
                "root_name": "补建订单",
                "file_name": "补建订单"
            },
            {
                "redis_key": "XMind_SupplementaryOrderCC",
                "root_name": "补建订单CC",
                "file_name": "补建订单CC"
            }
        ]
        self.test_result_summary = ''
        self.new_test_report_name = ''
        self.is_dd_push = is_dd_push

    def start(self):
        """测试开始"""
        print('========== 测试开始 ==========')

        os.environ['env'] = self.env
        # os.environ['debug'] = self.is_debug

    def end(self):
        """测试结束"""
        print('========== 测试结束 ==========')

    def get_discover(self):
        """生成测试套件集"""
        test_dir = self.d.get('test_dir')
        file_prefix = self.d.get('file_prefix')
        self.discover = unittest.defaultTestLoader.discover(start_dir=test_dir, pattern=file_prefix)
        # self.discover = unittest.TestLoader().discover(start_dir=test_dir, pattern=file_prefix)
        # self.discover = unittest.TestLoader().discover(start_dir='./BusinessModule', pattern='test*.py')

    def get_runner(self):
        """执行测试套件"""
        jsr = JsonTestRunner(**self.jtr_dict)
        jsr.run(self.discover)
        self.json_test_result = jsr.get_json_report()
        if self.is_print:
            print(
                json.dumps(
                    self.json_test_result,
                    sort_keys=True,
                    indent=4,
                    separators=(', ', ': '),
                    ensure_ascii=False
                )
            )
        else:
            pass

        try:
            jsr.generate_report(report_type='html')
        except BaseException as e:
            print('generate_report error:{}'.format(str(e)))

    def send_report(self):
        """发送邮件"""
        print('查找最新报告')
        new_test_report = BaseTools.latest_report(self.report_dir)
        new_xm = BaseTools.latest_report(self.xm_dir)
        print(new_test_report)
        self.new_test_report_name = new_test_report.split('/')[-1]
        mail_content = """{}\n{}\n测试人员:{}\n开始时间:{}\n结束时间:{}\n持续时间:{}\n总数:{}\n成功数:{}\n失败数:{}\n错误数:{}\n通过率:{}""".format(
            self.title,
            self.description,
            self.tester,
            self.json_test_result.get('start_time'),
            self.json_test_result.get('stop_time'),
            self.json_test_result.get('duration'),
            self.json_test_result.get('all_count'),
            self.json_test_result.get('success_count'),
            self.json_test_result.get('failure_count'),
            self.json_test_result.get('error_count'),
            self.json_test_result.get('pass_rate'),
        )
        if self.is_mail:
            print('发送报告到邮箱')
            SendEmail(DEBUG=self.is_debug).send_attach(
                html_file_path=new_test_report,
                mail_content=mail_content,
                xm_file_path=new_xm)
        else:
            print('不发送报告')

        self.test_result_summary = mail_content

        if self.is_dd_push:
            # print('调试:不钉钉推送')
            BaseTools.dd_push(report_result=self.test_result_summary, report_name=self.new_test_report_name)
        else:
            print('不钉钉推送')

    def generate_xmind(self):
        """生成XMind"""
        if self.is_xm:
            # xmind_keys = R.keys(pattern='XMind_*')
            for xm in self.xmind_dict:
                redis_key = xm.get('redis_key')
                if R.get(redis_key):
                    all_list = literal_eval(R.get(redis_key))
                    branch = gen_branch(all_list)
                    root_name = xm.get('root_name')
                    file_name = xm.get('file_name')
                    BaseTools.create_xm(branch, root_name=root_name, file_name=file_name)
                    R.delete(xm.get('redis_key'))
                    print('{}.XMind生成完毕'.format(file_name))
                else:
                    pass
        else:
            pass

    def main(self):
        """函数入口"""
        self.start()
        self.get_discover()
        self.get_runner()
        self.generate_xmind()
        self.send_report()
        self.end()


if __name__ == '__main__':
    """
    terminal execution command demo
    
    python3 run.py --title 平台发展自动化测试报告 --desc 交易域 --tester 杨跃雄 --is_print 1 --env uat --cf /Users/yangyuexiong/Desktop/KitDriverCase/business --mail 1
    
    python3 run.py --title 平台发展自动化测试报告 --desc 交易域 --tester 杨跃雄 --is_print 1 --env uat --cf /Users/yangyuexiong/Desktop/KitDriverCase/business
    
    python3 run.py --title 平台发展自动化测试报告 --desc 交易域 --tester 杨跃雄 --is_print 1 --env uat --cf /Users/yangyuexiong/Desktop/KitDriverCase/business --mail 1 --is_xm 1
    
    """
    main_init = gen_shell()
    # main_test = MainTest(**main_init)
    # main_test.main()
