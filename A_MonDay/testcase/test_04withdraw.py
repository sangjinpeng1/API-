import unittest
import requests
from unittestreport import list_data, ddt
from A_MonDay.common.handle_db import Handle_DB
from A_MonDay.common.handle_log import my_log
from A_MonDay.common.handle_tools import replace_data
from A_MonDay.common.handle_path import DATAS_DIR, os
from A_MonDay.common.handle_mysql import Handle_DB
from A_MonDay.common.fixtrue import BestTest
from A_MonDay.common.handle_excel import Handle_excel
from A_MonDay.common.handle_conf import conf


@ddt
class TestWithDraw(unittest.TestCase, BestTest):
    excel = Handle_excel(os.path.join(DATAS_DIR, 'test02.xlsx'), 'withdraw')
    cases = excel.read_excel()
    base_url = conf.get('env', 'base_url')

    @classmethod
    def setUpClass(cls) -> None:
        cls.user_login()

    @list_data(cases)
    def withdraw(self, item):
        url = self.base_url + item['url']
        method=item['method'].lower()
        expected=eval(item['expected'])
        if '#member_id#' in item['data']:
            item['data']=replace_data(item['data'],TestWithDraw)
            params=eval(item['data'])
        response=requests.request(url=url,json=params,method=method,headers=self.headers)


