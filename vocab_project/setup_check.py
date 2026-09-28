# -*- coding: utf-8 -*-
"""setup_check.py —— 环境自检脚本。
双击运行，看环境缺什么。仅用 Python 标准库。
"""
import sys
from pathlib import Path

from weekpath import root_path, data_path


def main():
    print("=" * 50)
    print("华文小助手 环境自检")
    print("=" * 50)
    print(f"Python 版本: {sys.version.split()[0]}")
    print(f"代码包根目录: {root_path()}")

    # 1) 检查标准库可用性
    for mod in ("csv", "pathlib", "collections"):
        try:
            __import__(mod)
            print(f"  [OK] 标准库 {mod} 可用")
        except ImportError as e:
            print(f"  [缺失] 标准库 {mod} 不可用: {e}")

    # 2) 检查 data/生词表.csv 是否存在
    csv_file = data_path("生词表.csv")
    if csv_file.exists():
        print(f"  [OK] 生词表存在: {csv_file}")
    else:
        print(f"  [缺失] 生词表不存在: {csv_file}")

    # 3) 试跑 vocab_tool
    print("-" * 50)
    print("试跑 vocab_tool.main() ...")
    try:
        import vocab_tool
        vocab_tool.main()
        out = root_path() / "练习.txt"
        if out.exists():
            print(f"  [OK] 已生成 {out}，大小 {out.stat().st_size} 字节")
        else:
            print("  [失败] 未生成 练习.txt")
    except Exception as e:
        print(f"  [错误] 运行失败: {type(e).__name__}: {e}")

    print("=" * 50)
    print("自检完成。")


if __name__ == "__main__":
    main()
