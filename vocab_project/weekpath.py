# -*- coding: utf-8 -*-
"""weekpath.py —— 统一代码包根目录定位工具。

从任何目录运行 vocab_tool.py，都能通过 root_path() 找到 data/ 目录。
"""
from pathlib import Path


def root_path() -> Path:
    """返回本代码包的根目录（即本文件所在目录）。"""
    return Path(__file__).resolve().parent


def data_path(filename: str) -> Path:
    """返回 data/ 目录下某个文件的完整路径。"""
    return root_path() / "data" / filename


if __name__ == "__main__":
    print("代码包根目录:", root_path())
    print("data 目录:", data_path("生词表.csv"))
