import pytest
from hanyu_lang.runtime import 解释器

def test_打印语句():
    引擎 = 解释器()
    assert 引擎.执行('打印("测试输出")') == "测试输出"

def test_变量赋值():
    引擎 = 解释器()
    assert 引擎.执行('数字 = 5\n 返回 数字') == 5