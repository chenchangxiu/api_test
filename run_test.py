# -*- coding: utf-8 -*-
# @Time     :2019/2/17 9:11 
# @Author   :changxiu chen
# @Email   :13532622590@139.com
# @File    :run_test.py
# @Software:PyCharm Community Edition
import unittest
from common import contants
from libext import HTMLTestRunnerNew

# 自动查找testcases目录下，以test开头的.py文件里面的测试类
discover=unittest.defaultTestLoader.discover(contants.cases_dir,pattern='test_*.py',top_level_dir=None)#pattern='test_*.py'表示模糊匹配
#使用上下文管理器
with open(contants.reports_html,'wb+') as file:
    runner=HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                              title='API',
                                              description='API测试报告',
                                              tester='陈昌秀')
    runner.run(discover)  # 执行查找到的用例