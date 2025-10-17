"""
SuperMro - Python 继承关系分析工具

一个用于分析Python项目类继承关系的工具，支持：
- 自动扫描Python包的类继承关系
- 生成MRO（Method Resolution Order）信息
- 可视化继承关系图
- 追踪方法在继承链中的定义位置
"""

__version__ = "0.1.0"
__author__ = "SuperMro Team"

from .analyzer import InheritanceAnalyzer
from .visualizer import InheritanceVisualizer
from .cli import main

__all__ = ["InheritanceAnalyzer", "InheritanceVisualizer", "main"]
