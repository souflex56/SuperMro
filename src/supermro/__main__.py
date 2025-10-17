#!/usr/bin/env python3
"""
SuperMro 主入口点

支持以下使用方式：
- python -m supermro
- python -m supermro --package myapp
- python -m supermro --visualize
"""

from .cli import main

if __name__ == "__main__":
    main()
