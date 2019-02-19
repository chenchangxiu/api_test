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
from common.config import ReadConfig
@ddt
class RechargeTest(unittest.TestCase):
    '充值接口类'
    # 获取测试数据
    cases = DoExcel(contants.cases_file, 'recharge').read_excel()
    @classmethod #调用累的时候只执行一次
    def setUpClass(cls):
        cls.request = HttpRequest()# 创建HttpRequest实例对象

    @classmethod
    def tearDownClass(cls):
        cls.request.session_close()#调用session_close()方法关闭会话机制,防止占用资源

    def setUp(self):
        print("------开始执行测试用例------")

    def tearDown(self):
        print("------测试用例执行结束------")

    @data(*cases)
    def test_run_cases(self,case):
        print("执行第{0}条测试用例,测试title是：{1}".format(case['id'],case['title']))
        #调用读取配置文件类
        read_config = ReadConfig()
        url = read_config.get('api', 'pre_url') +case['url']#URL进行拼接
        # 使用封装好的HttpRequest类中的http_request方法来完成请求
        res=self.request.http_request(case['method'],url,case['data'])
        #断言
        try:
            self.assertEqual(eval(case['ExpectedResult']),res.json())
            print("测试结果：Pass")
            TestResult = 'Pass'
        except Exception as e:
            print("执行接口测试期望结果与实际结果不一致：{0}".format(e))
            print("测试结果：Fail")
            TestResult = 'Fail'
            raise e
        finally:
            DoExcel(contants.cases_file, 'recharge').write_back(case['id'] + 1, 7, str(res.json()))  # 写入实际结果
            DoExcel(contants.cases_file, 'recharge').write_back(case['id'] + 1, 8, TestResult)  # 写入测试结论



