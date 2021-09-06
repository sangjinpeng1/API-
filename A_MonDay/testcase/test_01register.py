import unittest
import openpyxl
import random
import requests
from A_MonDay.common.handle_path import os, DATAS_DIR
from unittestreport import list_data, ddt
from A_MonDay.common.handle_excel import Handle_excel
from A_MonDay.common.handle_conf import conf
from A_MonDay.common.handle_tools import replace_data
from A_MonDay.common.handle_log import my_log
from A_MonDay.common.fixtrue import BestTest


@ddt
class TestRegister(unittest.TestCase):
    excel = Handle_excel(os.path.join(DATAS_DIR, 'test02.xlsx'), 'register')
    res = excel.read_excel()

    base_url = conf.get('env', 'base_url')
    headers = eval(conf.get('env', 'headers'))

    @list_data(res)
    def test_register(self, item):
        row = item['case_id'] + 1
        url = self.base_url + item['url']
        method = item['method'].lower()
        if '#mobile#' in item['data']:
            setattr(TestRegister, 'mobile', self.randomMobile())
            item['data'] = replace_data(item['data'], TestRegister)
        params = eval(item['data'])
        expected = eval(item['expected'])

        response = requests.request(url=url, method=method, headers=self.headers, json=params)
        res = response.json()

        try:
            self.asserDict(expected, res)
        except AssertionError as e:
            my_log.info('en')
            my_log.exception(e)
            self.excel.write_excel(row=row, column=9, value='未通过')
            raise e
        else:
            my_log.info('e11n')
            self.excel.write_excel(row=row, column=9, value='通过')

    # 断言是否包含
    def asserDict(self, expected, res):
        for k, v in expected.items():
            if res[k] == v:
                break
            else:
                raise AssertionError('{}not in {}'.format(expected, res))

    # 手机号
    def randomMobile(self):
        mobile = str(random.randint(13000000000, 13099999999))
        return mobile
