from configparser import ConfigParser
from handle_path import os, CONF_DIR


class Config(ConfigParser):
    # 在创建文件时，调用加载配置文件的内容
    def __init__(self, con_file):
        super().__init__()
        self.read(con_file, encoding='utf-8')

conf = Config(os.path.join(CONF_DIR, 'sang.ini'))
