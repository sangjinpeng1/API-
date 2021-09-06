import os
import logging
from handle_conf import conf
from handle_path import LOGS_DIR


def Creat_log(name, level, filename, sh_level, fh_level):
    log = logging.getLogger(name)
    log.setLevel(level)
    # 输出到控制台
    sh = logging.StreamHandler()
    sh.setLevel(sh_level)
    log.addHandler(sh)
    # 输出到文件
    fh = logging.FileHandler(filename)
    fh.setLevel(fh_level)
    log.addHandler(fh)
    # 设置输出格式
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(log_formatter)
    fh.setFormatter(log_formatter)

    return log

my_log=Creat_log(
    name=conf.get('logging', 'name'),
    level=conf.get('logging', 'level'),
    filename=os.path.join(LOGS_DIR, conf.get('logging', 'file')),
    sh_level=conf.get('logging', 'sh_level'),
    fh_level=conf.get('logging', 'fh_level')

)
