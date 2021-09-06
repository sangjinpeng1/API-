import unittest
import requests
from unittestreport import ddt,list_data
from A_MonDay.common.handle_log import my_log
from A_MonDay.common.handle_tools import replace_data
from A_MonDay.common.handle_path import os,DATAS_DIR
from A_MonDay.common.handle_excel import Handle_excel
from A_MonDay.common.handle_conf import conf

@ddt
class TestLogin(unittest.TestCase):
    excel=Handle_excel(os.path.join(DATAS_DIR,'test02.xlsx'),'login')
    cases=excel.read_excel()

    base_url=conf.get('env','url')
    headers=eval(conf.get('env','headers'))

    @list_data(cases)
    def test_login(self,item):
        url = self.base_url + item['url']
        method = item['method'].lower()
        params = eval(item['data'])
        data = eval(item['data'])

        response = requests.request(url=url, method=method, json=params, headers=self.headers)
        response.json()
        try:
            pass
        except AssertionError as e:
            pass
        else:
            pass

    def assertDict(self, expected, res):
        pass
