import re
from handle_conf import conf



def replace_data(data, cls):
    while re.search('#(.+?)#', data):
        res=re.search('#(.+?)#',data)
        # 要替换的参数
        item=res.group()
        # 被替换的参数
        attr=res.group(1)

        try:
            value=getattr(cls,attr)
        except AttributeError:
            value=conf.get('test_data',attr)
        data=data.replace(item,str(value))
    return data
        




