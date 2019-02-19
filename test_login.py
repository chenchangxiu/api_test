# -*- coding: utf-8 -*-
# @Time     :2019/1/21 18:18 
# @Author   :changxiu chen
# @Email   :13532622590@139.com
# @File    :test_recharge.py
# @Software:PyCharm Community Edition
import unittest
from ddt import ddt,data
from common.requests_class import HttpRequest
from common import contants
from common.do_excel_class import DoExcel
from common import logger

#引入日志
logger = logger.get_logger('LoginTest')
@ddt
class LoginTest(unittest.TestCase):
    '登录接口类'
    request = HttpRequest()  # 创建HttpRequest实例对象
    # 测试数据准备
    cases = DoExcel(contants.cases_file, 'login').read_excel()

    def setUp(self):
        logger.info("------开始执行测试用例------")

    def tearDown(self):
        logger.info("------测试用例执行结束------")

    @data(*cases)
    def test_run_cases(self,case):
        logger.info("执行第{0}条测试用例,测试title是：{1}".format(case['id'],case['title']))
        # 使用封装好的HttpRequest类中的http_request方法来完成请求
        res=self.request.http_request(case['method'],case['url'],case['data'])

        #断言
        try:
            self.assertEqual(eval(case['ExpectedResult']),res.json())
            logger.info("测试结果：Pass")
            TestResult = 'Pass'
        except Exception as e:
            logger.error("执行接口测试期望结果与实际结果不一致：{0}".format(e))
            logger.error("测试结果：Fail")
            TestResult = 'Fail'
        finally:
            DoExcel(contants.cases_file, 'login').write_back(case['id'] + 1, 7, str(res.json()))  # 写入实际结果
            DoExcel(contants.cases_file, 'login').write_back(case['id'] + 1, 8, TestResult)  # 写入测试结论






