# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 2:49 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : JsonTestRunner.py
# @Software: PyCharm

"""Github: https://github.com/yangyuexiong/JsonTestRunner"""

import io
import os
import sys
import json
import time
import platform
from datetime import datetime

import unittest
from unittest import TestResult

from global_env import PROJECT_NAME


class TemplateMixin:
    """HTML模版"""

    HTML_VUE_TMPL = r"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <!-- import CSS -->
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/element-ui@2.15.1/lib/theme-chalk/index.css"
    />

    <style>
      table table thead {
        display: none;
      }

      .el-table__expanded-cell[class*="cell"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-right: 0 !important;
      }

      .card {
        margin: 30px;
        white-space: pre;
      }
    </style>
  </head>
  <body>
    <div id="app">
      <el-backtop :bottom="10" :visibility-height="10"></el-backtop>
      <div>
        <h1>{{title}}</h1>
        <h3>测试人员 : {{tester}}</h3>
        <p>开始时间 : {{start_time}}</p>
        <p>合计耗时 : {{duration}}</p>
        <p>
          测试结果 : 共 {{all_count}}，通过 {{success_count}}，通过率
          {{pass_rate}}
        </p>
        <p>{{description}}</p>
      </div>

      <el-tabs type="border-card">
        <el-tab-pane :label="`所有(${all_count})`">
          <el-table
            :data="case_all_list"
            style="width: 100%; margin-bottom: 20px"
            border
            row-key="id"
          >
            <el-table-column type="expand">
              <template slot-scope="{row}">
                <el-table border :data="row.class_list" show-header="false">
                  <el-table-column type="expand">
                    <template slot-scope="{row}">
                      <el-table border :data="row.def_list" show-header="false">
                        <el-table-column type="expand">
                          <template slot-scope="{row}">
                            <el-card shadow="always" class="card">                              
                              <p v-for="i in row.output">{{i}}</p>
                            </el-card>
                          </template>
                        </el-table-column>
                         <!-- 中文 -->
                        <el-table-column
                          prop="case_method_name"
                        >
                          <template slot-scope="{row}">
                          {{row.case_method_name}} ({{row.case_method_doc}})
                        </template>
                      </el-table-column>
                      </el-table>
                    </template>
                  </el-table-column>
                  <!-- 中文 -->
                  <el-table-column prop="class_name">
                    <template slot-scope="{row}">
                      {{row.class_name}} ({{row.class_doc}})
                    </template>
                  </el-table-column>
                </el-table>
              </template>
            </el-table-column>
            <el-table-column prop="order_service" label="用例集/测试用例">
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane :label="`成功(${success_count})`"
          ><el-table
            :data="case_success_list"
            style="width: 100%; margin-bottom: 20px"
            border
            row-key="id"
          >
            <el-table-column type="expand">
              <template slot-scope="{row}">
                <el-table border :data="row.class_list" show-header="false">
                  <el-table-column type="expand">
                    <template slot-scope="{row}">
                      <el-table border :data="row.def_list" show-header="false">
                        <el-table-column type="expand">
                          <template slot-scope="{row}">
                            <el-card shadow="always" class="card">
                              <p v-for="i in row.output">{{i}}</p>
                            </el-card>
                          </template>
                        </el-table-column>
                         <!-- 中文 -->
                        <el-table-column
                          prop="case_method_name"
                        >
                          <template slot-scope="{row}">
                          {{row.case_method_name}} ({{row.case_method_doc}})
                        </template>
                      </el-table-column>
                      </el-table>
                    </template>
                  </el-table-column>
                  <!-- 中文 -->
                  <el-table-column prop="class_name">
                    <template slot-scope="{row}">
                      {{row.class_name}} ({{row.class_doc}})
                    </template>
                  </el-table-column>
                </el-table>
              </template>
            </el-table-column>
            <el-table-column prop="order_service" label="用例集/测试用例">
            </el-table-column> </el-table
        ></el-tab-pane>
        <el-tab-pane :label="`失败(${fail_count})`"
          ><el-table
            :data="case_fail_list"
            style="width: 100%; margin-bottom: 20px"
            border
            row-key="id"
          >
            <el-table-column type="expand">
              <template slot-scope="{row}">
                <el-table border :data="row.class_list" show-header="false">
                  <el-table-column type="expand">
                    <template slot-scope="{row}">
                      <el-table border :data="row.def_list" show-header="false">
                        <el-table-column type="expand">
                          <template slot-scope="{row}">
                            <el-card shadow="always" class="card">
                              <p v-for="i in row.output">{{i}}</p>
                            </el-card>
                          </template>
                        </el-table-column>
                         <!-- 中文 -->
                        <el-table-column
                          prop="case_method_name"
                        >
                          <template slot-scope="{row}">
                          {{row.case_method_name}} ({{row.case_method_doc}})
                        </template>
                      </el-table-column>
                      </el-table>
                    </template>
                  </el-table-column>
                   <!-- 中文 -->
                  <el-table-column prop="class_name">
                    <template slot-scope="{row}">
                      {{row.class_name}} ({{row.class_doc}})
                    </template>
                  </el-table-column>
                </el-table>
              </template>
            </el-table-column>
            <el-table-column prop="order_service" label="用例集/测试用例">
            </el-table-column> </el-table
        ></el-tab-pane>
      </el-tabs>
    </div>
  </body>
  <!-- import Vue before Element -->
  <script src="https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.min.js"></script>
  <!-- import JavaScript -->
  <script src="https://cdn.jsdelivr.net/npm/element-ui@2.15.1/lib/index.js"></script>

"""

    def __init__(self, test_result):
        if isinstance(test_result, dict):
            self.test_result = test_result
        else:
            raise TypeError('test_result 应该是一个 dict 类型')

    @classmethod
    def __generate_script(cls, **kwargs):
        """script"""

        # demo
        """
        new Vue({
          el: "#app",
          data: function () {
            return {
              title: "title",
              tester: "yyx",
              description:"【请下载附件,查看报告明细。】",
              start_time: "2020-04-17 14:17:33",
              pass_rate: "60.5%",
              duration: "0:06:36.007642",
              all_count: "100",
              success_count: "50",
              fail_count: "50",
              case_all_list,
              case_success_list,
              case_fail_list,
            };
          },
            methods: {},
        });
        """

        data = """
              title: "{title}",
              tester: "{tester}",
              description: "{description}",
              start_time: "{start_time}",
              pass_rate: "{pass_rate}",
              duration: "{duration}",
              all_count: "{all_count}",
              success_count: "{success_count}",
              fail_count: "{fail_count}",
              case_all_list,
              case_success_list,
              case_fail_list,
        """.format(
            title=kwargs.get('title'),
            tester=kwargs.get('tester'),
            description=kwargs.get('description'),
            start_time=kwargs.get('start_time'),
            pass_rate=kwargs.get('pass_rate'),
            duration=kwargs.get('duration'),
            all_count=kwargs.get('all_count'),
            success_count=kwargs.get('success_count'),
            fail_count=kwargs.get('failure_count'),
        )

        script = r"""
        <script>
        var case_all_list = {};
        var case_success_list = {};
        var case_fail_list = {};
        
        {}
          {}
          {}
            {}
              {}
            {}
          {}
        {}
        </script>  
        """.format(
            kwargs.get('result_list'),
            kwargs.get('result_success_list'),
            kwargs.get('result_fail_list'),
            "new Vue({",
            """el: "#app",""",
            """data: function () {""",
            """return {""",
            data,
            """};""",
            """},""",
            """});""",
        )
        return script

    def generate_html_report(self):
        """生成html报告"""
        tr = self.test_result
        # print(tr)
        title = tr.get('title')
        description = tr.get('description')
        tester = tr.get('tester')
        start_time = tr.get('start_time')
        stop_time = tr.get('stop_time')
        duration = tr.get('duration')
        all_count = tr.get('all_count')
        success_count = tr.get('success_count')
        failure_count = tr.get('failure_count')
        error_count = tr.get('error_count')
        pass_rate = tr.get('pass_rate')
        result_list = tr.get('result_list')
        result_code = tr.get('result_code')

        script = self.__generate_script(**tr)
        html_vue = self.HTML_VUE_TMPL + '\n' + script + '\n' + "</html>"

        return html_vue


class OutputRedirector:
    """重定向标准输出或标准错误"""

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


class TestResultExtension(TestResult):

    def __init__(self, verbosity=1):
        super().__init__()
        self.verbosity = verbosity
        self.this_stdout = None
        self.this_stderr = None
        self.output_buffer = None
        self.stdout_redirect = sys.stdout
        self.stderr_redirect = sys.stderr

        self.all_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0

        self.result_all_list = []
        self.result_success_list = []
        self.result_fail_list = []

    def assemble_result_obj(self, test, result_code, output, _traceback=None):

        module = test.__module__
        class_name = test.__class__.__name__
        class_doc = test.__class__.__doc__ if test.__class__.__doc__ else ''
        case_method_name = test._testMethodName
        case_method_doc = test._testMethodDoc if test._testMethodDoc else ''

        if isinstance(output, list):
            output.append(_traceback)
        else:
            pass
        result_obj = {
            'order_service': module,
            'class_name': class_name,
            'class_doc': class_doc,
            'result_code': result_code,
            'case_method_name': case_method_name,
            'case_method_doc': case_method_doc,
            'output': output
        }
        if result_code == 0:
            self.result_success_list.append(result_obj.copy())
        else:
            self.result_fail_list.append(result_obj.copy())

        self.result_all_list.append(result_obj.copy())

    def complete_output(self):
        """断开输出重定向和返回缓冲区,分别独立打印输出"""

        if self.this_stdout:
            sys.stdout = self.this_stdout
            sys.stderr = self.this_stderr
            self.this_stdout = None
            self.this_stderr = None
        return self.output_buffer.getvalue()

    def startTest(self, test):
        super().startTest(test)
        self.output_buffer = io.StringIO()  # 每次创建一个新的 StringIO 空间
        stdout_redirector.fp = self.output_buffer  # StringIO实例
        stderr_redirector.fp = self.output_buffer  # StringIO实例
        self.this_stdout = sys.stdout
        self.this_stderr = sys.stderr
        sys.stdout = stdout_redirector  # 将 StringIO 的值输出
        sys.stderr = stderr_redirector  # 将 StringIO 的值输出

    def stopTest(self, test):
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        super().addSuccess(test)
        output = self.complete_output()
        output = output.split('\n')

        self.assemble_result_obj(test, 0, output, '')
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        output = output.split('\n')

        self.assemble_result_obj(test, 1, output, _exc_str)
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        output = output.split('\n')

        self.assemble_result_obj(test, 2, output, _exc_str)
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')


class JsonTestRunner:
    """
    Github: https://github.com/yangyuexiong/JsonTestRunner

    接收一个unittest测试套件,生成json格式的测试结果,包含HTML,XML的测试报告

    例子:
        # 测试套件集合
        discover = unittest.defaultTestLoader.discover('./test_path', pattern='test*.py')

        # JsonTestRunner实例化执行
        jtr = JsonTestRunner(result_format='json', title='自动化测试报告', description='xxx描述', tester='杨跃雄')
        jtr.run(discover)

    json:
        jtr.run(discover)
        jtr.get_json_report()

    报告生成:
        jtr.generate_report('html')
        jtr.generate_report('xml')
        jtr.generate_report('excel')

    """
    default_title = '测试报告'
    default_description = '描述...'
    default_tester = '测试人员'

    def __init__(self, title=None, description=None, tester=None):
        """
        :title: 报告标题(默认-default_title)
        :description: 报告描述内容(默认-default_description)
        :tester: 测试人员(默认-default_tester)
        """

        if not title:
            self.title = self.default_title
        else:
            self.title = title

        if not description:
            self.description = self.default_description
        else:
            self.description = description

        if not tester:
            self.tester = self.default_tester
        else:
            self.tester = tester

        self.start_time = datetime.now()
        self.stop_time = 0
        self.duration = 0
        self.test_result = {}

    def run(self, test):
        """
        :test: 测试套件
        运行Unittest的测试用例或测试套件
        """
        # result = _TestResult(1)
        # result = TestResult()
        result = TestResultExtension(1)
        test(result)
        self.stop_time = datetime.now()
        self.generate_result(result)
        print('\nTime Elapsed: {}'.format(self.duration), file=sys.stderr)

    def generate_result(self, result):
        """输出 json 格式的测试结果(用于多方对接与扩展使用)"""
        self.stop_time = datetime.now()
        self.duration = str(self.stop_time - self.start_time)
        success_count = result.success_count
        failure_count = result.failure_count + result.error_count
        error_count = result.error_count
        all_count = success_count + failure_count + error_count
        pass_rate = str("%.2f%%" % (float(success_count) / float(all_count) * 100))

        rl = result.result_all_list
        sl = result.result_success_list
        fl = result.result_fail_list
        all_list = self.__zip_test_result(rl)
        success_list = self.__zip_test_result(sl)
        fail_list = self.__zip_test_result(fl)

        test_result = {
            "start_time": str(self.start_time)[:19],
            "stop_time": str(self.stop_time)[:19],
            "duration": self.duration,
            "all_count": all_count,
            "success_count": success_count,
            "failure_count": failure_count,
            # "error_count": error_count,
            "pass_rate": pass_rate,
            "result_list": all_list,
            "result_success_list": success_list,
            "result_fail_list": fail_list,
        }
        self.test_result = test_result

    def get_json_report(self):
        """获取 json 报告"""
        print(self.get_json_report.__doc__)
        return self.test_result

    def __generate_html_report(self, report_path=None):
        """生成 HTML 报告"""
        print(self.__generate_html_report.__doc__)

        self.test_result['title'] = self.title
        self.test_result['description'] = self.description
        self.test_result['tester'] = self.tester
        html_test_report = TemplateMixin(test_result=self.test_result)
        content = html_test_report.generate_html_report()

        with open(report_path, 'wb') as f:
            f.write(content.encode('utf8'))

    def __generate_xml_report(self, report_path=None):
        """生成 XML 报告"""
        print(self.__generate_xml_report.__doc__)
        # TODO 渲染 XML

    def __generate_excel_report(self, report_path=None):
        """生成 Excel 报告"""
        print(self.__generate_excel_report.__doc__)
        # TODO 渲染 Excel

    def generate_report(self, report_type=None, report_name=None):
        """
        生成报告
        :report_type:可选(html,xml,excel)
        :report_name:报告名称
        """
        report_path = os.getcwd()
        ts = time.strftime('%Y-%m-%d_%H_%M_%S')
        html_report_name = 'create_{}_'.format(ts) + report_name if report_name else 'Test_Report_{}_.html'.format(ts)
        xml_report_name = 'create_{}_'.format(ts) + report_name if report_name else 'Test_Report_{}_.xml'.format(ts)
        excel_report_name = 'create_{}_'.format(ts) + report_name if report_name else 'Test_Report_{}_.xlsx'.format(ts)
        report_path = report_path.split(PROJECT_NAME)[0] + '{}/reports'.format(PROJECT_NAME)

        report_type_dict = {
            "html": {
                "report_name": html_report_name,
                "report_path": report_path,
                "func": self.__generate_html_report
            },
            "xml": {
                "report_name": xml_report_name,
                "report_path": report_path,
                "func": self.__generate_xml_report
            },
            "excel": {
                "report_name": excel_report_name,
                "report_path": report_path,
                "func": self.__generate_excel_report
            }
        }
        if report_type in list(report_type_dict.keys()) and isinstance(report_type, str):
            rt = report_type_dict.get(report_type.lower())
        else:
            rt = report_type_dict.get('html')

        rp = rt.get('report_path')
        rn = rt.get('report_name')
        final_path = '{}/{}'.format(rp, rn)
        print('报告名称:{}'.format(rt.get('report_name')))
        print('目录路径:{}'.format(rt.get('report_path')))
        print('绝对路径:{}'.format(final_path))

        generate_report_func = rt.get('func')
        generate_report_func(report_path=final_path)

    @staticmethod
    def __zip_test_result(rl):
        current_module = {}
        new_list = []
        rl.append({})

        for index, i in enumerate(rl, 1):
            current_module['id'] = index
            if index == 1:
                current_module['order_service'] = i.get('order_service')
                current_module['class_list'] = []
                class_obj = {
                    "class_name": i.get('class_name'),
                    "class_doc": i.get('class_doc'),
                    "def_list": []
                }
                try:
                    del i['class_name']
                    del i['class_doc']
                    del i['order_service']
                except BaseException as e:
                    pass
                class_obj['def_list'].append(i)
                current_module['class_list'].append(class_obj)

            else:
                if current_module.get('order_service') == i.get('order_service'):
                    class_name = current_module.get('class_list')[-1].get('class_name')
                    def_list = current_module.get('class_list')[-1].get('def_list')
                    if class_name == i.get('class_name'):
                        try:
                            del i['class_name']
                            del i['class_doc']
                            del i['order_service']
                        except BaseException as e:
                            pass
                        def_list.append(i)
                    else:
                        class_obj = {
                            "class_name": i.get('class_name'),
                            "class_doc": i.get('class_doc'),
                            "def_list": []
                        }
                        try:
                            del i['class_name']
                            del i['class_doc']
                            del i['order_service']
                        except BaseException as e:
                            pass
                        class_obj['def_list'].append(i)
                        current_module['class_list'].append(class_obj)

                else:
                    new_list.append(current_module.copy())
                    current_module.clear()

                    current_module['order_service'] = i.get('order_service')
                    current_module['class_list'] = []
                    class_obj = {
                        "class_name": i.get('class_name'),
                        "class_doc": i.get('class_doc'),
                        "def_list": []
                    }
                    try:
                        del i['class_name']
                        del i['class_doc']
                        del i['order_service']
                    except BaseException as e:
                        pass
                    class_obj['def_list'].append(i)
                    current_module['class_list'].append(class_obj)

        return new_list


if __name__ == '__main__':
    # 例子
    if platform.system() == "Darwin":
        start_dir = '/Users/yangyuexiong/Desktop/{}/business'.format(PROJECT_NAME)
    else:
        start_dir = r"\{}\business".format(PROJECT_NAME)

    discover = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern='test*.py')
    # discover.run(TestResult())

    jtr = JsonTestRunner(tester='杨跃雄')
    jtr.run(discover)
    print(jtr.get_json_report())

    result_list = jtr.get_json_report().get('result_list')
    print(json.dumps(result_list, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))

    jtr.generate_report('html')
    # jtr.generate_report('xml')
    # jtr.generate_report('excel')
