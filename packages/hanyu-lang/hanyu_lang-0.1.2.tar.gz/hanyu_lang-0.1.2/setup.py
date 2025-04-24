# -*- coding: utf-8 -*-
from setuptools import setup, find_packages, Command
from setuptools.extension import Extension
import os
import shutil

def 读取文件(文件名):
    """统一处理文件编码问题"""
    with open(
        os.path.join(os.path.dirname(__file__), 文件名), 
        encoding="utf-8"
    ) as f:
        return f.read()

class CleanCommand(Command):
    """增强版清理命令"""
    user_options = []
    
    def initialize_options(self):
        self.cwd = None
    
    def finalize_options(self):
        self.cwd = os.getcwd()
    
    def run(self):
        assert os.getcwd() == self.cwd, '必须在项目根目录执行'
        待删除目录 = [
            'build', 'dist', 'src/hanyu_lang.egg-info',
            '.pytest_cache', '__pycache__'
        ]
        for 目录 in 待删除目录:
            if os.path.exists(目录):
                print(f'删除目录: {目录}')
                shutil.rmtree(目录, ignore_errors=True)
        
        # 递归清理编译产物
        for 根目录, _, 文件列表 in os.walk("."):
            for 文件 in 文件列表:
                if 文件.endswith((".pyc", ".so", ".pyd")):
                    完整路径 = os.path.join(根目录, 文件)
                    print(f'删除文件: {完整路径}')
                    os.remove(完整路径)

setup(
    name="hanyu-lang",
    version="0.1.2",
    author="你的名字/团队名",
    author_email="your.email@example.com",
    description="汉语编程语言实现",
    long_description=读取文件("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hanyu-lang",
    license="MIT",
    license_files=["LICENSE"],

    # 包结构配置（关键修改）
    packages=find_packages(where="src", include=["hanyu_lang*"]) + [
        "hanyu_lang",  # 主包
        "hanyu_lang.runtime",  # 运行时子包
        "hanyu_gui"    # GUI包
    ],
    package_dir={
        "hanyu_lang": "src/hanyu_lang",
        "hanyu_gui": "gui"
    },
    include_package_data=True,
    
    # 数据文件配置
    package_data={
        "hanyu_lang": ["examples/*.汉语", "docs/*.md"],
        "hanyu_gui": ["assets/*.ico", "themes/*.json"]
    },
    
    # 依赖配置
    python_requires=">=3.8",
    setup_requires=["Babel"],
    install_requires=[
        "pygments>=2.7",
        "watchdog>=2.0",
        "tkinterweb>=3.11"  # GUI增强依赖
    ],
    
    # 入口点配置（需同步修改以下文件）
    entry_points={
        "console_scripts": [
            "hanyu=hanyu_lang.cli:main",  # 对应src/hanyu_lang/cli.py中的main函数
            "hanyu-gui=hanyu_gui.main_window:启动"  # 修改gui/main_window.py添加启动函数
        ],
    },
    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Compilers"
    ],
    cmdclass={
        'clean': CleanCommand,
    },
    
    # C扩展配置（需创建src/hanyu_lang/accelerate.c）
    #ext_modules=[
    #Extension(
    #    "hanyu_lang.accelerate",
     #   sources=["src/hanyu_lang/accelerate.c"],  # 确保路径正确
     #   extra_compile_args=["/Ox" if os.name == 'nt' else "-O3"]
    #)
    #] if os.path.exists("src/hanyu_lang/accelerate.c") else [],
    
    # 安全扩展
    extras_require={
        "secure": ["pyjwt>=2.0", "cryptography>=3.4"],
        "full": ["numpy>=1.21", "pandas>=1.3"]
    },
    
    # 国际化支持
    #data_files=[
#("share/locale/zh_CN/LC_MESSAGES", 
#["translations/zh_CN/LC_MESSAGES/hanyu.mo"])
#],
    # 添加关键配置 ↓
    zip_safe=False,  # 禁用压缩包模式
    use_2to3=False,  # 禁用自动转换

)