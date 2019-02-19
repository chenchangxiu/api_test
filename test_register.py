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
from common.mysql_class import MysqlUtil
@ddt
class RegisterTest(unittest.TestCase):
    '注册接口类'
    request = HttpRequest()  # 创建HttpRequest实例对象
    # 获取测试数据
    cases = DoExcel(contants.cases_file, 'register').read_excel()
    # 创建数据连接
    mysql=MysqlUtil()
    sql = "select max(mobilephone) from future.member"  # 查询最大手机号
    max = mysql.fetch_one(sql)[0]  # 执行SQL，并且返回最近的一条数据，是元祖，使用下标取第一个值

    def setUp(self):
        print("------开始执行测试用例------")

    def tearDown(self):
        print("------测试用例执行结束------")

    @data(*cases)
    def test_run_cases(self,case):
        print("执行第{0}条测试用例,测试title是：{1}".format(case['id'],case['title']))

        #实现手机号参数化，保证该手机号没有被注册
        data_dict = eval(case['data'])#这里case['data']是str类型，需要转换成字典
        if data_dict['mobilephone'] == '${register_mobile}':  # 判断是否等于标记
            data_dict['mobilephone'] = int(self.max) + 1  # 将最大手机号码+1 赋值给mobilephone

        #使用封装好的HttpRequest类中的http_request方法来完成请求
        res=self.request.http_request(case['method'],case['url'],data_dict)
        #断言
        try:
            self.assertEqual(eval(case['ExpectedResult']),res.json())
            print("测试结果：Pass")
            TestResult = 'Pass'
        except Exception as e:
            print("执行接口测试期望结果与实际结果不一致：{0}".format(e))
            print("测试结果：Fail")
            TestResult = 'Fail'
        finally:
            DoExcel(contants.cases_file, 'register').write_back(case['id'] + 1, 7, str(res.json()))  # 写入实际结果
            DoExcel(contants.cases_file, 'register').write_back(case['id'] + 1, 8, TestResult)  # 写入测试结论



