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
class TestWithdraw(unittest.TestCase):
    excel = Handle_excel(os.path.join(DATAS_DIR, 'test02.xlsx'), 'withdraw')
    res = excel.read_excel()
    base_url = conf.get('env', 'base_url')
    db = Handle_DB()

    @classmethod
    def setUp(cls):
        url = conf.get('env', 'base_url') + '/member/login'
        params = {
            "mobile_phone": conf.get('test_data', 'mobile'),
            "pwd": conf.get('test_data', 'pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        token = jsonpath(res, '$..token')[0]
        headers['Authorization'] = token
        cls.headers = headers
        member_id = jsonpath(res, '$..id')[0]
        cls.member_id = member_id

    @list_data(res)
    def test_withdraw(self, item):
        url = self.base_url + item['url']
        method = item['method']
        if '#member_id#' in item['data']:
            item['data'] = item['data'].replace('#member_id#', str(self.member_id))

        params = eval(item['data'])
        expected = eval(item['expected'])
        sql = 'select leave_amount from futureloan.member where mobile_phone="{}"'.format(
            conf.get("test_data", "mobile"))
        start_amout = self.db.find_one(sql)[0]
        print('用户执行之前，用户的余额：', start_amout)

        response = requests.request(url=url, method=method, json=params, headers=self.headers)
        res = response.json()
        end_amout = self.db.find_one(sql)[0]
        print('用户执行之后，用户的余额：', end_amout)

        try:
            self.assertEquals(expected['code'], res['code'])
            self.assertEquals(expected['msg'], res['msg'])
            if res['msg'] == 'OK':
                self.assertEquals(float(start_amout - end_amout), params['amount'])
                print(params, params['amount'])
            else:
                self.assertEquals(float(end_amout - start_amout), 0)
        except AssertionError as e:
            my_log.exception(e)
            raise e
        else:
            my_log.info('quxiansuccess')
