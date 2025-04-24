# -*- coding: utf-8 -*-
import argparse
import sys
from pathlib import Path
from .runtime import 解释器

def main():
    parser = argparse.ArgumentParser(prog="hanyu")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    run_parser = subparsers.add_parser("run", help="执行汉语代码文件")
    run_parser.add_argument("filepath", type=Path, help="代码文件路径")
    
    args = parser.parse_args()
    
    if args.command == "run":
        if not args.filepath.exists():
            print(f"错误：文件 {args.filepath} 不存在")
            sys.exit(1)
            
        with open(args.filepath, "r", encoding="utf-8") as f:
            代码内容 = f.read()
        
        引擎 = 解释器()
        执行结果 = 引擎.执行(代码内容)
        print(执行结果)

if __name__ == "__main__":
    main()