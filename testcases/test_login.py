import unittest
import requests
from unittestreport import ddt,list_data
from handle_excel import Handle_excel
from handle_log import my_log
from handle_conf import conf
from handle_path import os,DATAS_DIR,CONF_DIR
@ddt
class TestLogin(unittest.TestCase):
    excel=Handle_excel(os.path.join(DATAS_DIR,'test02.xlsx'),'login')
    res=excel.read_excel()

    base_url=conf.get('env','base_url')
    headers=eval(conf.get('env','headers'))
    @list_data(res)
    def testlogin(self,item):
        url = self.base_url + item['url']
        method=item['method'].lower()
        params=eval(item['data'])
        data=eval(item['data'])

        response=requests.request(url=url,method=method,json=params,headers=self.headers)
        response.json()
        try:
            pass
        except AssertionError as e:
            pass
        else:
            pass

    def assertDict(self,expected,res):
        pass


