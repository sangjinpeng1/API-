import unittest
import requests
from unittestreport import list_data, ddt
from A_MonDay.common.handle_conf import conf
from A_MonDay.common.handle_excel import Handle_excel
from A_MonDay.common.handle_path import DATAS_DIR, os
from A_MonDay.common.fixtrue import BestTest
from A_MonDay.common.handle_tools import replace_data
from A_MonDay.common.handle_log import my_log
from A_MonDay.common.handle_db import Handle_DB


@ddt
class TestRecharge(unittest.TestCase, BestTest):
    excel = Handle_excel(os.path.join(DATAS_DIR, 'test02.xlsx'), 'recharge')
    cases = excel.read_excel()
    url = conf.get('env', 'base_url')
    db = Handle_DB()

    @classmethod
    def setUpClass(cls) -> None:
        cls.user_login()

    @list_data(cases)
    def test_recharge(self, item):
        row = item['case_id'] + 1
        url = self.url + item['url']
        method = item['method'].lower()
        item['data'] = replace_data(item['data'], TestRecharge)
        params = eval(item['data'])
        expected = eval(item['expected'])
        sql = 'select leave_amount from futureloan.member where mobile_phone="{}"'.format(
            conf.get('test_data', 'mobile'))
        start_amount = self.db.find_one(sql)[0]
        response = requests.request(url=url, method=method, json=params, headers=self.headers)
        end_amount = self.db.find_one()[0]
        res = response.json()

        try:
            self.assertIn(expected, res)
            self.assertEquals(expected['msg'],res['msg'])
            if res['msg']=='ok':
                self.assertEquals(float(end_amount-start_amount),params['amount'])
            else:
                self.assertEquals(float(end_amount - start_amount),0)

        except Exception as e:
            my_log.info('hi')
            my_log.exception(e)
            raise e
        else:
            my_log.info('hi')
