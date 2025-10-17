#!/usr/bin/env python3
"""
SuperMro 安装脚本

使用方法：
    python install.py

或者直接安装：
    pip install -e .
"""

import subprocess
import sys
import os
from pathlib import Path


def install_supermro():
    """安装SuperMro"""
    print("🚀 正在安装 SuperMro...")
    
    try:
        # 安装依赖
        print("📦 安装依赖...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        # 安装SuperMro
        print("🔧 安装SuperMro...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        
        print("✅ SuperMro 安装成功！")
        print("\n🎉 现在您可以在任何Python项目目录中使用：")
        print("   python -m supermro")
        print("   supermro --help")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {e}")
        return False
    
    return True


def main():
    """主函数"""
    print("=" * 50)
    print("🧬 SuperMro - Python 继承关系分析工具")
    print("=" * 50)
    
    if install_supermro():
        print("\n📖 查看使用说明：")
        print("   python -m supermro --help")
        print("\n📚 查看文档：")
        print("   cat README.md")
    else:
        print("\n❌ 安装失败，请检查错误信息")


if __name__ == "__main__":
    main()
