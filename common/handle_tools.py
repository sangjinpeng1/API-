import re
from handle_conf import conf

# class TestData:
#     id = 1
#     name = 'zhangsan1'
#     age = 19

# def replace_data(data,cls):
#         # 匹配并返回第一个符合规则的匹配对象
#     while re.search('#(.+?)#',data):
#         res=re.search('#(.+?)#',data)
#         item=res.group()
#         attr=res.group(1)
#         try:
#             value=getattr(cls,attr)
#         except AttributeError:
#             value=conf.get('test_data',attr)
#         # 进行替换
#         data=data.replace(item,str(value))
#     return data

#
#
# if __name__=='__main__':
#     str1 = "'id':'#id#','name':'#name#','age':'#age#'"
#     res=replace_data(str1,TestData)
#     print(res)


def replace_data(data,cls):
    # 匹配并返回第一个符合规则的匹配对象
    while re.search('#(.+?)#',data):
        res=re.search('#(.+?)#',data)
        item=res.group()
        attr=res.group(1)
        try:
            value=getattr(cls,attr)
        except AttributeError:
            value=conf.get('test_data',attr)
            # 进行替换
        data=data.replace(item,str(value))
    return data



