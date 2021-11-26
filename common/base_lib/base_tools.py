# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 3:05 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : base_tools.py
# @Software: PyCharm


import os
import platform
import smtplib
from datetime import datetime
from ast import literal_eval
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests
import xmind

from global_env import PROJECT_NAME, DING_TALK_URL, AT_MOBILES, AT_USER_IDS, IS_AT_ALL
from config.config import get_config

conf = get_config()


def gen_single_tree(_list):
    """
    生成单树
    """
    _list.reverse()
    current_list = []
    for index, i in enumerate(_list):
        if current_list:
            topics = [current_list[0]]
            single_tree = {
                "id": index,
                "name": i,
                # "link": None,
                # "title": "",
                # "note": None,
                # "label": None,
                # "comment": None,
                # "markers": [],
                "topics": topics
            }
            current_list.clear()
            current_list.append(single_tree)
        else:
            single_tree = {
                "id": index,
                "name": i,
                # "link": None,
                # "title": "",
                # "note": None,
                # "label": None,
                # "comment": None,
                # "markers": [],
                "topics": []
            }
            current_list.append(single_tree)

    # print(json.dumps(current_list[0], sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
    return current_list[0]


def gen_many_tree(data_list, result_list):
    """
    合并树:
    JS:
        function genTree(data, result) {
            data.forEach((item, i) => {
              const { name, topics } = item;
              const _result = result.find(item => item.name === name);
              if (_result) {
                if (item.topics.length) {
                  genTree(item.topics, _result.topics);
                }
              } else {
                result.push({
                  name,
                  topics: topics
                });
              }
            });

            return result;
          }
    """

    for data in data_list:
        name = data.get('name')
        topics = data.get('topics')
        flag = False
        _result = None
        for result in result_list:
            if result.get('name') == name:
                flag = True
                _result = result
                break
        if flag:
            if len(topics) > 0:
                gen_many_tree(topics, _result.get('topics'))
        else:
            result_list.append({
                "name": name,
                # "link": None,
                # "title": "",
                # "note": None,
                # "label": None,
                # "comment": None,
                # "markers": [],
                "topics": topics
            })
    return result_list


def gen_branch(all_list):
    """
    创建XMind完整分支
    :all_list:元数据 例如: ['正课', '国内', '需要地址', '新用户']
    """

    def _gen_for(x):
        if isinstance(x, list):
            for i in x:
                _gen_for(i)
        elif isinstance(x, dict):
            name = x.get('name')
            if isinstance(name, str):
                _gen_for(x.get('topics'))
            elif isinstance(name, list):
                x['name'] = '\n'.join(name)
        else:
            pass

    single_tree_list = []
    for i in all_list:
        single_tree_list.append(gen_single_tree(i))

    branch_list = gen_many_tree(single_tree_list, [])

    for b in branch_list:
        _gen_for(b)
    # print(branch_list)

    return branch_list


def gen_xm(parent, data):
    """
    :parent:需要绑定的父节点
    :data:子dict数据
    """

    f_topic = parent.addSubTopic()
    f_topic.setTitle(data.get('name'))
    topics = data.get('topics')
    if topics:
        for t in topics:
            gen_xm(f_topic, t)
    else:
        pass


class SendEmail:
    """
    发送邮件
    """

    def __init__(self, YYX=False, DEBUG=True):

        self.YYX = YYX
        self.DEBUG = DEBUG

        if self.YYX:
            self.mail_from = '872540033@qq.com'  # 发件邮箱账号
            self.mail_pwd = ''  # 发件邮箱的授权码
        else:
            self.mail_from = 'yuexiong.yang@happy-seed.com'  # 发件邮箱账号
            self.mail_pwd = ''  # 发件邮箱的授权码

        if self.DEBUG:  # True
            self.to_list = conf.get('mail', 'TO_LIST_DEBUG')
            self.ac_list = conf.get('mail', 'AC_LIST_DEBUG')
        else:  # False
            self.to_list = conf.get('mail', 'TO_LIST')
            self.ac_list = conf.get('mail', 'AC_LIST')

        self.subject = '自动化测试报告'  # 邮件标题

    @classmethod
    def open_test_report(cls, file_path):
        """打开最新测试报告"""
        f = open(file_path, 'rb')  # 打开最新报告
        print('打开报告', f)
        mail_content = f.read()  # 读取->作为邮件内容
        f.close()
        return mail_content

    def send_attach(self, html_file_path, mail_content=None, xm_file_path=None):
        """
        附件发送
        :param html_file_path:
        :param mail_content:
        :param xm_file_path:
        :return:
        """

        to_list = literal_eval(self.to_list)
        ac_list = literal_eval(self.ac_list)

        to = ",".join(to_list)  # 收件人
        acc = ",".join(ac_list)  # 抄送人

        # mail_content = cls.open_test_report(file_path)

        message = MIMEMultipart()
        # message['From'] = Header("基础服务" + "<" + '杨跃雄' + ">", 'utf-8')
        # message['To'] = Header("yyx", 'utf-8')
        message['From'] = Header("自动化测试", 'utf-8')
        message['To'] = to
        message['Cc'] = acc
        message['Subject'] = Header(self.subject, 'utf-8')
        # message.attach(MIMEText(mail_content, 'html', 'utf-8'))
        message.attach(MIMEText(mail_content, 'plain', 'utf-8'))
        # message.attach(MIMEText('基础服务:自动化测试报告-邮件内容', 'plain', 'utf-8'))  # 邮件内容

        if html_file_path:
            # 附件:HTML
            att_html = MIMEText(open(html_file_path, 'rb').read(), 'base64', 'utf-8')
            att_html["Content-Type"] = 'application/octet-stream'
            att_html["Content-Disposition"] = 'attachment; filename=' + html_file_path.split(
                'reports\\' if platform.system() == "Windows" else 'reports/')[1]
            message.attach(att_html)
        if xm_file_path:
            pass
            # TODO XMind上传
            # 附件:XMind
            # att_xm = MIMEText(open(xm_file_path, 'rb').read(), 'base64', 'utf-8')
            # att_xm["Content-Type"] = 'application/octet-stream'
            # att_xm["Content-Disposition"] = 'attachment; filename=' + xm_file_path.split('xminds/')[1]
            # message.attach(att_xm)

        try:
            # smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
            smtpObj = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
            smtpObj.login(self.mail_from, self.mail_pwd)
            smtpObj.sendmail(self.mail_from, message['To'].split(',') + message['Cc'].split(','), message.as_string())
            print('发送成功')
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print("发送失败:{}".format(str(e)))

    def send_normal(self, subject, content):
        """
        正常发送
        :param subject:
        :param content:
        :return:
        """
        to = ",".join(literal_eval(self.to_list))
        message = MIMEText(content)
        message["Subject"] = subject
        message["From"] = self.mail_from
        message["To"] = to
        message['Cc'] = ",".join(literal_eval(self.ac_list))
        try:
            smtpObj = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
            smtpObj.login(self.mail_from, self.mail_pwd)
            smtpObj.sendmail(self.mail_from, to, message.as_string())
            print("发送成功!")
            smtpObj.quit()
        except BaseException as e:
            print("发送失败:{}".format(str(e)))


class BaseTools:
    """
    通用工具类
    """

    @classmethod
    def latest_report(cls, report_dir):
        """
        查找最新报告
        :param report_dir: 报告路径
        :return:
        """
        # print(report_dir)
        lists = os.listdir(report_dir)  # 报告列表
        if lists:
            # print('报告列表', lists)
            lists.sort(key=lambda fn: os.path.getmtime(
                report_dir + '\\' + fn if platform.system() == "Windows" else report_dir + '/' + fn))  # 排序
            # print('排序后报告列表', lists)
            file = os.path.join(report_dir, lists[-1])  # 最新生成的报告
            print('最新的报告', file)
            return file
        else:
            return lists

    @classmethod
    def create_xm(cls, data, root_name, file_name):
        """
        :data:数据list
        :root_name:模块名称
        :file_name:文件名称
        """

        def __save():
            fn = file_name if '.xmind' in file_name else file_name + '.xmind'
            ph = "{}/{}".format(os.getcwd().split(PROJECT_NAME)[0] + PROJECT_NAME + '/xminds', fn)
            xmind.save(workbook, ph)

        workbook = xmind.load("temp.xmind")
        sheet = workbook.getPrimarySheet()
        root = sheet.getRootTopic()
        root.setTitle(root_name)
        for i in data:
            gen_xm(root, i)
        __save()

    @classmethod
    def dd_push(cls, report_result, report_name, markdown_text=None):
        """钉钉推送"""
        if platform.system() == "Linux":
            report_url = 'http://10.4.184.48:8000/{}'.format(report_name)
        else:
            report_url = os.getcwd().split(PROJECT_NAME)[0] + PROJECT_NAME + '/reposts/{}'.format(report_name)

        url = DING_TALK_URL

        if not url.strip():
            raise TypeError('钉钉推送失败: DING_TALK_URL 未配置')

        headers = {"Content-Type": "application/json;charset=utf-8"}

        msg = """{}\n报告地址: {}""".format(report_result, report_url)
        """
        json_data = {
            "msgtype": "text",
            "text": {
                "content": msg
            },
            "at": {
                "atMobiles": AT_MOBILES,
                "atUserIds": AT_USER_IDS,
                "isAtAll": IS_AT_ALL
            }
        }

        
        """

        demo_text = "#### 测试报告:{}  \n  > 测试人员:{}  \n  > 开始时间:{}  \n  > 结束时间:{}  \n  > 持续时间:{}  \n  > 总数:{}  \n  > 成功数:{}  \n  > 失败数:{}  \n  > 错误数:{}  \n  > 通过率:{}  \n  > 报告地址:[前往](1)"

        report_link = "  \n  > 报告地址:[{}]({})".format(report_url, report_url)

        json_data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "测试报告",
                "text": markdown_text + report_link
            },
            "at": {
                "atMobiles": AT_MOBILES,
                "atUserIds": AT_USER_IDS,
                "isAtAll": IS_AT_ALL
            }
        }
        response = requests.post(url, json=json_data, headers=headers)
        print(response.json())


if __name__ == '__main__':
    pass
