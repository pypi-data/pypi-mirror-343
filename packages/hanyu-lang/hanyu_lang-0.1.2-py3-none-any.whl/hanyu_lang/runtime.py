# -*- coding: utf-8 -*-
class 解释器:
    def __init__(self):
        self.变量表 = {}
    
    def 执行(self, 代码: str) -> str:
        try:
            if '打印(' in 代码 and '"' in 代码:
                return 代码.split('"')[1]
            return "执行完成"
        except Exception as e:
            return f"错误: {str(e)}"