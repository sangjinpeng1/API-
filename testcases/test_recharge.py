import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from handle_excel import Handle_excel
from handle_log import my_log
from handle_conf import conf
from handle_path import DATAS_DIR
from handle_tools import replace_data


@ddt
class TestRecharge(unittest.TestCase):
    excel = Handle_excel(os.path.join(DATAS_DIR, 'test02.xlsx'), 'recharge')
    res = excel.read_excel()
    base_url = conf.get('env', 'base_url')

    @classmethod
    def setUpClass(cls):
        # 用例类的前置方法，登录提取token
        # 1.请求登录接口，进行登录
        url = conf.get('env', 'base_url') + '/member/login'
        params = {
            "mobile_phone": conf.get('test_data', 'mobile'),
            "pwd": conf.get('test_data', 'pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        # 登录成功后去提取token
        token = jsonpath(res, '$..token')[0]
        # 将token添加到请求头中
        headers['Authorization'] = 'Bearer ' + token
        # 保存含有token的请求头为类属性
        cls.headers = headers
        # 3.
        # 提取用户id给后面的接口使用
        member_id = jsonpath(res, '$..id')[0]
        cls.member_id = member_id

    @list_data(res)
    def test_recharge(self, item):
        url = self.base_url + item['url']
        method = item['method'].lower()
        # 数据替换
        # item['data']=replace_data(item['data'],TestRecharge)
        item['data']=replace_data(item['data'],TestRecharge)
        params = eval(item['data'])
        expected = eval(item['expected'])
        response = requests.request(url=url, method=method, json=params, headers=self.headers)
        res = response.json()

        try:
            self.assertInt(expected, res)
        except AssertionError as e:
            my_log.info('hi')
            my_log.exception(e)
            raise e
        else:
            my_log.info('hi')

    def assertInt(self, expected, res):
        for k, v in expected.items():
            if res[k] == v:
                break
            else:
                raise AssertionError('{}not in {}'.format(expected, res))
