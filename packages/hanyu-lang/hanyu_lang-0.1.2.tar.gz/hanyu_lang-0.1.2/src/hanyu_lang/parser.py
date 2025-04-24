# -*- coding: utf-8 -*-

# 语法解析器
class 解析器:
    def __init__(self, 令牌列表):
        self.令牌列表 = 令牌列表
        self.pos = 0
    
    def 解析(self):
        语法树 = []
        while self.当前令牌() is not None:
            # 新增变量赋值判断
            if self.当前类型() == '标识符' and self.下一个类型() == '赋值符':
                语法树.append(self.解析赋值())
            elif self.当前类型() == 'PRINT':
                语法树.append(self.解析打印())
        return 语法树
    
    def 解析赋值(self):
        变量名 = self.当前词()
        self.消耗('标识符')
        self.消耗('赋值符')
        # 解析右侧表达式（简化版只处理数字）
        值 = self.当前词()
        self.消耗('数字')
        # 获取字符串内容
        if self.当前类型() != 'STRING':
            raise SyntaxError(f"第{self.当前令牌()[2]}行: 需要字符串参数")
        内容 = self.当前令牌()[1]
        self.消耗('STRING')
        self.消耗('RPAREN')
        return ('赋值', 变量名, 值)

    def 当前行号(self):
        return self.当前令牌()[2] if self.当前令牌() else 0
    
    def 当前词(self):
        return self.当前令牌()[1] if self.当前令牌() else None
    
    def 当前令牌(self):
        return self.令牌列表[self.pos] if self.pos < len(self.令牌列表) else None
    
    def 当前类型(self):
        return self.当前令牌()[0] if self.当前令牌() else None
    
    def 消耗(self, 预期类型):
        if self.当前类型() == 预期类型:
            self.pos += 1
        else:
            当前行 = self.当前令牌()[2] if self.当前令牌() else '未知'
            raise SyntaxError(f"第{当前行}行: 预期{预期类型}，实际是{self.当前类型()}")
