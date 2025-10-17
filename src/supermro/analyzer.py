#!/usr/bin/env python3
"""
继承关系分析器

提供核心的继承关系分析功能，支持：
- 扫描Python包的类继承关系
- 生成MRO信息
- 追踪方法定义位置
"""

import sys
import pkgutil
import importlib
import inspect
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


class InheritanceAnalyzer:
    """继承关系分析器"""
    
    def __init__(self, project_path: str = "."):
        """
        初始化分析器
        
        Args:
            project_path: 项目路径，默认为当前目录
        """
        self.project_path = Path(project_path).resolve()
        self._add_project_to_path()
    
    def _add_project_to_path(self):
        """将项目路径添加到Python路径中"""
        if str(self.project_path) not in sys.path:
            sys.path.insert(0, str(self.project_path))
    
    def find_python_packages(self) -> List[str]:
        """
        查找项目中的Python包
        
        Returns:
            包名列表
        """
        packages = []
        
        # 查找当前目录下的Python包
        for item in self.project_path.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                packages.append(item.name)
        
        # 查找子目录中的包
        for item in self.project_path.rglob("__init__.py"):
            if item.parent != self.project_path:
                rel_path = item.parent.relative_to(self.project_path)
                package_name = ".".join(rel_path.parts)
                packages.append(package_name)
        
        return sorted(packages)
    
    def analyze_package(self, package_name: str) -> Dict[str, Any]:
        """
        分析指定包的继承关系
        
        Args:
            package_name: 包名
            
        Returns:
            分析结果字典
        """
        try:
            package = importlib.import_module(package_name)
        except Exception as e:
            return {"error": f"无法导入包 {package_name}: {e}"}
        
        result = {
            "package_name": package_name,
            "modules": {},
            "classes": {},
            "inheritance_chains": {}
        }
        
        # 扫描包中的所有模块
        for _, module_name, _ in pkgutil.walk_packages(package.__path__, package_name + "."):
            try:
                module = importlib.import_module(module_name)
                module_info = self._analyze_module(module, package_name)
                if module_info["classes"]:
                    result["modules"][module_name] = module_info
            except Exception as e:
                print(f"⚠️ 跳过模块 {module_name}: {e}")
                continue
        
        # 构建继承链
        result["inheritance_chains"] = self._build_inheritance_chains(result["modules"])
        
        return result
    
    def _analyze_module(self, module, package_name: str) -> Dict[str, Any]:
        """分析单个模块"""
        module_file = getattr(module, '__file__', 'unknown')
        file_name = Path(module_file).name if module_file != 'unknown' else 'unknown'
        
        classes = {}
        
        for name, cls in inspect.getmembers(module, inspect.isclass):
            # 只处理在当前模块中定义的类
            if (cls.__module__.startswith(package_name) and 
                cls.__module__ == module.__name__):
                
                # 获取类的方法
                methods = [method for method in dir(cls) 
                          if not method.startswith('_') and 
                          callable(getattr(cls, method, None))]
                
                classes[name] = {
                    "name": cls.__name__,
                    "module": cls.__module__,
                    "file": file_name,
                    "methods": methods,
                    "mro": [c.__name__ for c in cls.mro()],
                    "bases": [base.__name__ for base in cls.__bases__]
                }
        
        return {
            "file": file_name,
            "classes": classes
        }
    
    def _build_inheritance_chains(self, modules: Dict[str, Any]) -> Dict[str, List[str]]:
        """构建继承链"""
        chains = {}
        
        for module_name, module_info in modules.items():
            for class_name, class_info in module_info["classes"].items():
                chains[class_name] = class_info["mro"]
        
        return chains
    
    def trace_method(self, class_name: str, method_name: str, 
                    package_name: str) -> Optional[Dict[str, Any]]:
        """
        追踪方法在继承链中的定义位置
        
        Args:
            class_name: 类名
            method_name: 方法名
            package_name: 包名
            
        Returns:
            追踪结果
        """
        try:
            # 查找类
            cls = self._find_class(class_name, package_name)
            if not cls:
                return {"error": f"未找到类 {class_name}"}
            
            # 追踪方法
            method_chain = []
            for c in cls.mro():
                if method_name in c.__dict__:
                    module = inspect.getmodule(c)
                    file_path = getattr(module, '__file__', '(built-in)')
                    method_chain.append({
                        "class": c.__name__,
                        "module": c.__module__,
                        "file": file_path
                    })
            
            return {
                "class": class_name,
                "method": method_name,
                "chain": method_chain
            }
            
        except Exception as e:
            return {"error": f"追踪方法时出错: {e}"}
    
    def _find_class(self, class_name: str, package_name: str):
        """查找指定类"""
        try:
            package = importlib.import_module(package_name)
            for _, module_name, _ in pkgutil.walk_packages(package.__path__, package_name + "."):
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, class_name):
                        return getattr(module, class_name)
                except Exception:
                    continue
        except Exception:
            pass
        return None
    
    def print_analysis(self, package_name: str):
        """打印分析结果"""
        result = self.analyze_package(package_name)
        
        if "error" in result:
            print(f"❌ 分析失败: {result['error']}")
            return
        
        print(f"\n📦 扫描包：{package_name}\n{'='*60}")
        
        for module_name, module_info in result["modules"].items():
            print(f"\n📁 模块: {module_name} ({module_info['file']})")
            for class_name, class_info in module_info["classes"].items():
                print(f"\n🧩 类: {class_name}")
                for base in class_info["mro"]:
                    print("   →", base)
        
        print("\n✅ 扫描完成\n")
