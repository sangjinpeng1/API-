import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from handle_conf import conf
from handle_excel import Handle_excel
from handle_log import my_log
from handle_mysql import Handle_DB
from handle_path import DATAS_DIR
from handle_tools import replace_data


@ddt
class Test_Audit(unittest.TestCase):
    excel = Handle_excel(os.path.join(DATAS_DIR, 'test02.xlsx'), 'audit')
    res = excel.read_excel()
    db = Handle_DB()

    @classmethod
    def setUpClass(cls) -> None:
        #         管理员登陆
        url = conf.get('env', 'base_url') + '/member/login'
        params = {
            'mobile_phone': conf.get('test_data', 'admin_mobile'),
            'pwd': conf.get('test_data', 'admin_pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        admin_token = jsonpath(res, '$..token')[0]
        headers['Authorization'] = 'Bearer ' + admin_token
        cls.admin_headers = headers
        cls.admin_member_id = jsonpath(res, '$..id')[0]

        #         普通用户登录
        params = {
            'mobile_phone': conf.get('test_data', 'mobile'),
            'pwd': conf.get('test_data', 'pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        token = jsonpath(res, '$..token')[0]
        headers['Authorization'] = 'Bearer ' + token
        cls.headers = headers
        cls.member_id = jsonpath(res, '$..id')[0]

    def setUp(self) -> None:
        #             用例级别的前置
        url = conf.get('env', 'base_url') + '/loan/add'
        params = {
            'member_id': self.member_id,
            'title': '借钱实现财富自由',
            'amount': 2000,
            'loan_rate': 12.0,
            'loan_term': 3,
            'loan_date_type': 1,
            'bidding_days': 5
        }
        response = requests.post(url=url, json=params, headers=self.headers)
        res = response.json()
        Test_Audit.loan_id = jsonpath(res, '$..id')[0]

    @list_data
    def test_audit(self, item):
        url = conf.get('env', 'base_url') + item['url']
        item['data'] = replace_data(item['data'], Test_Audit)
        params = eval(item['data'])
        method = item['method']
        expected = eval(item['expected'])
        response = requests.request(url=url, json=params, method=method, headers=self.admin_headers)
        res = response.json()
        if res['msg']=='OK' and item['title']=='审核通过':
            Test_Audit.pass_loan_id=params['loan_id']
        try:
            self.assertEquals(expected['code'],res['code'])
            self.assertEquals(expected['msg'],res['msg'])
            if item['check_sql']:
                sql=item['check_sql'].format(self.loan_id)
                status=self.db.find_one(sql)[0]
                self.assertEquals(expected['status'],status)

        except AssertionError as e:
            my_log.info('直行通过')
        else:
            my_log.info('执行失败')
