import os

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COMMON_DIR = os.path.join(BASE_DIR, 'common')
CONF_DIR = os.path.join(BASE_DIR, 'config')
DATAS_DIR = os.path.join(BASE_DIR, 'datas')
LOGS_DIR = os.path.join(BASE_DIR, 'log')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
CASES_DIR = os.path.join(BASE_DIR, 'testcase')
print(CASES_DIR)