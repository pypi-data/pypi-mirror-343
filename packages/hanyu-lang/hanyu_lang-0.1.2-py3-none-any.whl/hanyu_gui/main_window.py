# -*- coding: utf-8 -*-
import sys
import os
import traceback  # 新增导入

import tkinter as tk
from pathlib import Path
from tkinter import ttk
from ..src.runtime import 运行时环境
from pkg_resources import resource_filename


# ----------- 新增的关键代码 -----------
# 获取项目根目录并加入系统路径
BASE_DIR = Path(__file__).parent.parent  # 定位到F:\LKSYS\Hanyu-Lang
sys.path.append(str(BASE_DIR))  # 使Python能识别src模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 关键修复

# 修正为（使用包名导入）：
from hanyu_lang.lexer import 分析
from hanyu_lang.parser import 解析器
from hanyu_lang.runtime import 运行时环境
# -----------------------------------

class 开发环境:
    def __init__(self):
        # 添加DPI感知（在创建窗口前）
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.窗口 = tk.Tk()
        self.窗口.tk.call('tk', 'scaling', 2.0)  # 200%缩放
        self.窗口.title("汉语编程环境")
        self.窗口.iconbitmap(
            resource_filename("hanyu_gui", "assets/app.ico")
        )
        # 代码编辑区
        self.编辑器 = tk.Text(self.窗口, height=30, width=80)
        self.编辑器.pack(pady=10)
        
        # 运行按钮
        self.运行按钮 = ttk.Button(
            self.窗口, 
            text="运行", 
            command=self.运行代码
        )
        self.运行按钮.pack()
        
        # 输出区
        self.输出区 = tk.Text(self.窗口, height=10, state='disabled')
        self.输出区.pack(pady=5)

        # 新增菜单栏
        self.菜单栏 = tk.Menu(self.窗口)
        self.文件菜单 = tk.Menu(self.菜单栏, tearoff=0)
        self.文件菜单.add_command(label="保存", command=self.保存代码)
        self.文件菜单.add_command(label="打开", command=self.打开文件)
        self.菜单栏.add_cascade(label="文件", menu=self.文件菜单)
        self.窗口.config(menu=self.菜单栏)

    def 保存代码(self):
        文件路径 = tk.filedialog.asksaveasfilename(
            defaultextension=".汉语",
            filetypes=[("汉语代码文件", "*.汉语")]
        )
        if 文件路径:
            with open(文件路径, "w", encoding="utf-8") as f:
                f.write(self.编辑器.get("1.0", "end-1c"))
    
    def 打开文件(self):
        文件路径 = tk.filedialog.askopenfilename(
            filetypes=[("汉语代码文件", "*.汉语")]
        )
        if 文件路径:
            with open(文件路径, "r", encoding="utf-8") as f:
                self.编辑器.delete(1.0, tk.END)
                self.编辑器.insert(tk.END, f.read())

    def 运行代码(self):
        代码 = self.编辑器.get("1.0", "end-1c")
        try:
            from src.lexer import 分析
            from src.parser import 解析器
            from src.runtime import 运行时环境

            令牌 = 分析(代码)
            print("【词法分析结果】", 令牌)  # 新增
            语法树 = 解析器(令牌).解析()
            print("【语法树】", 语法树)  # 新增
            环境 = 运行时环境()

            # 执行代码（新增部分）
            执行结果 = 执行器().执行(语法树)
            print("【执行结果】", 执行结果)  # 新增
            print(sys.path)  # 查看路径是否包含项目根目录

            # 显示输出
            self.输出区.config(state='normal')
            self.输出区.delete(1.0, tk.END)
            self.输出区.insert(tk.END, f"执行成功！输出：{执行结果}")
            self.输出区.config(state='disabled')
            self.显示输出(f"执行成功！\n变量表：{环境.变量表}")

        except Exception as e:
            self.输出区.config(state='normal', fg='red')# 红色错误提示
            self.输出区.delete(1.0, tk.END)
            error_msg = f"错误：{str(e)}\n追踪：{traceback.format_exc()}"
            self.输出区.insert(tk.END, error_msg)
            self.输出区.insert(tk.END, f"错误：{str(e)}")
            if '行' in str(e):  # 从错误信息提取行号
                行号 = str(e).split('行')[0].replace('第','')
                self.显示错误(str(e), 行号=行号)
            else:
                self.显示错误(str(e))
        finally:
            self.输出区.config(state='disabled')

# 在类定义末尾添加
@classmethod
def 启动(cls):
    app = cls()
    app.窗口.mainloop()

if __name__ == "__main__":
    开发环境.启动()
    app = 开发环境()
    app.窗口.mainloop()

