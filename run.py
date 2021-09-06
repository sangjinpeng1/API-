import unittest
from unittestreport import TestRunner
from handle_path import CASES_DIR, REPORTS_DIR
from unittestreport.core.sendEmail import SendEmail


def main():
    suite = unittest.defaultTestLoader.discover(CASES_DIR)
    runner = TestRunner(suite,
                        filename='login.html',
                        report_dir=REPORTS_DIR,
                        tester='xiaolin',
                        title='标题'
                        )
    runner.run()
    em = SendEmail(host='smtp.qq.com',
                   port=465,
                   user='z534310117@qq.com',
                   password='szellqianefkcaeb')
    em.send_email(subject='测试报告', content='测试内容', filename=None, to_addrs='z534310117@qq.com')
    # runner.send_email(host='smtp.qq.com',
    #                   port=465,
    #                   user='z534310117@qq.com',
    #                   password='szellqianefkcaeb',
    #                   to_addrs='z534310117@qq.com',
    #                   is_file=True)
    # 钉钉添加机器人，自定义机器人，关键字  ‘测试’
    # webhook = '钉钉链接'
    # runner.dingtalk_notice(url=webhook, key='测试')



if __name__ == '__main__':
    main()
