# -*- coding: utf-8 -*-

# 词法分析器
# 中文关键词定义
关键词 = {
    '如果': 'IF',
    '否则': 'ELSE',
    '循环': 'WHILE',
    '定义函数': 'DEF',
    '打印': 'PRINT'
}

符号映射 = {
    '(': 'LPAREN',
    ')': 'RPAREN',
    '+': 'PLUS',
    '-': 'MINUS',
    '=': 'EQUALS'
}

def 分析(代码):
    令牌列表 = []
    行号 = 1
    pos = 0
    长度 = len(代码)
    while pos < 长度:
        char = 代码[pos]
        # 跳过空格
        if char.isspace():
            if char == '\n':
                行号 += 1
            pos += 1
        # 处理字符串（关键修正）
        elif char in ['"', '“', '”']:  # 同时支持中英文引号
            引号类型 = char
            start = pos + 1
            pos += 1  # 跳过起始引号
            while pos < 长度 and 代码[pos] != 引号类型:
                pos += 1
            if pos >= 长度:
                raise SyntaxError(f"第{行号}行: 字符串未闭合")
            内容 = 代码[start:pos]
            令牌列表.append(('STRING', 内容, 行号))
            pos += 1  # 跳过闭合引号
        # 处理符号（必须放在中文关键词前）
        elif char in 符号映射:
            令牌列表.append((符号映射[char], char, 行号))
            pos += 1
        # 识别中文关键词
        elif char.isalpha():
            start = pos
            while pos < 长度 and 代码[pos].isalpha():
                pos += 1
            词 = 代码[start:pos]
            if 词 in 关键词:
                令牌列表.append((关键词[词], 词, 行号))
            else:
                令牌列表.append(('标识符', 词, 行号))
        # 其他字符暂不处理
        else:
            pos += 1
    return 令牌列表