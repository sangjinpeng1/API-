import re


# str1='123456asdfg#123#,#45#5das'
#
# res1=re.findall('#.+?#',str1)
# print(res1)


class TestData:
    id = 1
    name = 'zhangsan1'
    age = 19


str1 = "'id':'#id#','name':'#name#','age':'#age#'"

# 匹配并返回第一个符合规则的匹配对象
res2 = re.search('#(.+?)#', str1)
print(res2)
# group(): 提取匹配对象中的内容
item=res2.group()
print('被替换的内容:',item)
# 替换的内容
attr=res2.group(1)
print('替换的内容:',attr)
# 替换内容对应的值
value=getattr(TestData,attr)
print('替换内容对应的值:',value)

res3=str1.replace(item,str(value))
print(res3)

























