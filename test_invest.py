# -*- coding: utf-8 -*-
# @Time     :2019/2/16 16:37 
# @Author   :changxiu chen
# @Email   :13532622590@139.com
# @File    :test_invest.py
# @Software:PyCharm Community Edition
import unittest
from ddt import ddt,data
from common.requests_class import HttpRequest
from common import contants
from common.do_excel_class import DoExcel
from common.config import ReadConfig
from common import context
from common.context import Context
from common.mysql_class import MysqlUtil
@ddt
class Invest_Test(unittest.TestCase):
    '充值接口类'
    # 获取测试数据
    cases = DoExcel(contants.cases_file, 'invest').read_excel()
    @classmethod #调用累的时候只执行一次
    def setUpClass(cls):
        cls.request = HttpRequest()# 创建HttpRequest实例对象
        cls.mysql=MysqlUtil()

    @classmethod
    def tearDownClass(cls):
        cls.request.session_close()#调用session_close()方法关闭会话机制,防止占用资源
        cls.mysql.close()

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

        #查找参数化的测试数据，进行动态替换
        data=context.replace(case['data'])

        # 使用封装好的HttpRequest类中的http_request方法来完成请求
        res=self.request.http_request(case['method'],url,data)
        #断言
        try:
            self.assertEqual(case['ExpectedResult'],int(res.json()['code']))
            print("测试结果：Pass")
            TestResult = 'Pass'
            #判断是否加标成功，如果成功就按照借款人的ID去数据库查询最新的标记录
            if res.json()['msg'] == '加标成功':
                loan_member_id = getattr(Context, 'loan_member_id')
                sql = "select id from future.loan where memberID='{0}'" \
                      " order by createTime desc limit 1".format(loan_member_id)
                loan_id = self.mysql.fetch_one(sql)[0]
                setattr(Context, 'loan_id',str(loan_id))  # 转成str，后续通过正则替换
        except Exception as e:
            print("执行接口测试期望结果与实际结果不一致：{0}".format(e))
            print("测试结果：Fail")
            TestResult = 'Fail'
            raise e
        finally:
            DoExcel(contants.cases_file, 'invest').write_back(case['id'] + 1, 7,str(res.json()['code'])) # 写入实际结果
            DoExcel(contants.cases_file, 'invest').write_back(case['id'] + 1, 8, TestResult)  # 写入测试结论
