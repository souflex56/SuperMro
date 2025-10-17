#!/usr/bin/env python3
"""
命令行接口

提供命令行交互功能，支持：
- 自动检测Python包
- 交互式选择分析目标
- 生成可视化图
- 方法追踪
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional

from .analyzer import InheritanceAnalyzer
from .visualizer import InheritanceVisualizer


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description="SuperMro - Python 继承关系分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python -m supermro                    # 在当前目录分析
  python -m supermro --package myapp   # 分析指定包
  python -m supermro --visualize       # 生成可视化图
  python -m supermro --trace           # 追踪方法定义
        """
    )
    
    parser.add_argument(
        "--package", "-p",
        help="要分析的包名（可选，不指定则自动检测）"
    )
    
    parser.add_argument(
        "--visualize", "-v",
        action="store_true",
        help="生成可视化图"
    )
    
    parser.add_argument(
        "--trace", "-t",
        action="store_true",
        help="追踪方法定义"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径"
    )
    
    parser.add_argument(
        "--project-path",
        default=".",
        help="项目路径（默认为当前目录）"
    )
    
    args = parser.parse_args()
    
    # 创建分析器
    analyzer = InheritanceAnalyzer(args.project_path)
    
    # 自动检测包
    if not args.package:
        packages = analyzer.find_python_packages()
        if not packages:
            print("❌ 未找到Python包，请确保当前目录包含Python包")
            return
        
        if len(packages) == 1:
            package_name = packages[0]
            print(f"🔍 自动检测到包: {package_name}")
        else:
            print("🔍 发现多个包:")
            for i, pkg in enumerate(packages, 1):
                print(f"  {i}. {pkg}")
            
            try:
                choice = input("请选择要分析的包 (输入数字): ").strip()
                package_name = packages[int(choice) - 1]
            except (ValueError, IndexError):
                print("❌ 无效选择，使用第一个包")
                package_name = packages[0]
    else:
        package_name = args.package
    
    # 分析包
    print(f"\n📦 开始分析包: {package_name}")
    analyzer.print_analysis(package_name)
    
    # 生成可视化图
    if args.visualize:
        print("\n🎨 生成可视化图...")
        visualizer = InheritanceVisualizer()
        analysis_result = analyzer.analyze_package(package_name)
        
        if "error" not in analysis_result:
            output_file = visualizer.visualize_project_mro(
                analysis_result, 
                args.output
            )
            if output_file:
                print(f"✅ 可视化图已保存: {output_file}")
        else:
            print(f"❌ 无法生成可视化图: {analysis_result['error']}")
    
    # 方法追踪
    if args.trace:
        print("\n🔍 方法追踪模式")
        try:
            class_name = input("请输入类名: ").strip()
            method_name = input("请输入方法名: ").strip()
            
            if class_name and method_name:
                result = analyzer.trace_method(class_name, method_name, package_name)
                if "error" in result:
                    print(f"❌ {result['error']}")
                else:
                    print(f"\n🔍 {class_name}.{method_name}() 调用顺序:")
                    for item in result["chain"]:
                        print(f"  🧭 {item['class']}.{method_name}() 定义于 {item['file']}")
            else:
                print("❌ 类名和方法名不能为空")
        except (EOFError, KeyboardInterrupt):
            print("\n跳过方法追踪")


def interactive_mode():
    """交互式模式"""
    print("🚀 SuperMro - Python 继承关系分析工具")
    print("=" * 50)
    
    # 获取项目路径
    project_path = input("请输入项目路径 (回车使用当前目录): ").strip()
    if not project_path:
        project_path = "."
    
    analyzer = InheritanceAnalyzer(project_path)
    
    # 查找包
    packages = analyzer.find_python_packages()
    if not packages:
        print("❌ 未找到Python包")
        return
    
    print(f"\n🔍 发现 {len(packages)} 个包:")
    for i, pkg in enumerate(packages, 1):
        print(f"  {i}. {pkg}")
    
    # 选择包
    try:
        choice = input(f"\n请选择要分析的包 (1-{len(packages)}): ").strip()
        package_name = packages[int(choice) - 1]
    except (ValueError, IndexError):
        print("❌ 无效选择，使用第一个包")
        package_name = packages[0]
    
    # 分析
    analyzer.print_analysis(package_name)
    
    # 询问是否生成可视化图
    try:
        visualize = input("\n是否生成可视化图？(y/n): ").strip().lower()
        if visualize == "y":
            print("\n🎨 生成可视化图...")
            visualizer = InheritanceVisualizer()
            analysis_result = analyzer.analyze_package(package_name)
            
            if "error" not in analysis_result:
                visualizer.visualize_project_mro(analysis_result)
            else:
                print(f"❌ 无法生成可视化图: {analysis_result['error']}")
    except (EOFError, KeyboardInterrupt):
        print("\n跳过可视化生成")
    
    # 询问是否追踪方法
    try:
        trace = input("\n是否追踪某个类的方法定义？(y/n): ").strip().lower()
        if trace == "y":
            class_name = input("请输入类名: ").strip()
            method_name = input("请输入方法名: ").strip()
            
            if class_name and method_name:
                result = analyzer.trace_method(class_name, method_name, package_name)
                if "error" in result:
                    print(f"❌ {result['error']}")
                else:
                    print(f"\n🔍 {class_name}.{method_name}() 调用顺序:")
                    for item in result["chain"]:
                        print(f"  🧭 {item['class']}.{method_name}() 定义于 {item['file']}")
            else:
                print("❌ 类名和方法名不能为空")
    except (EOFError, KeyboardInterrupt):
        print("\n跳过方法追踪")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 无参数时使用交互式模式
        interactive_mode()
    else:
        # 有参数时使用命令行模式
        main()
