import unittest
import os
import requests
import random
from unittestreport import ddt,list_data
from handle_excel import Handle_excel
from handle_log import my_log
from handle_conf import conf
from handle_path import DATAS_DIR

@ddt
class TestRegister(unittest.TestCase):
    excel=Handle_excel(os.path.join(DATAS_DIR,'test02.xlsx'),'register')
    res=excel.read_excel()

    base_url=conf.get('env','base_url')
    headers=eval(conf.get('env','headers'))

    @list_data(res)
    def test_register(self,item):
        row=item['case_id']+1
        url=self.base_url+item['url']
        method=item['method']
        if '#mobile#' in item['data']:
            mobile=self.randomMobile()
            item['data']=item['data'].replace('#mobile#',mobile)
        params=eval(item['data'])
        print(params)
        expected=eval(item['expected'])
        response=requests.request(method, url,json=params,headers=self.headers)
        res=response.json()

        try:
            self.asserDict(expected,res)
        except AssertionError as e:
            my_log.info('diu')
            my_log.exception(e)
            self.excel.write_excel(row=row,column=9,value='未通过')
            raise e
        else:
            my_log.info('good')
            self.excel.write_excel(row=row, column=9, value='通过')

    def asserDict(self,expected,res):
        for k,v in expected.items():
            if res[k]==v:
                break
            else:
                raise AssertionError('{}not in {}'.format(expected, res))

    def randomMobile(self):
        mobile=str(random.randint(13000000000,13099999999))
        return mobile














