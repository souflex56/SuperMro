"""
测试继承分析器
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from supermro.analyzer import InheritanceAnalyzer


class TestInheritanceAnalyzer:
    """测试继承分析器"""
    
    def setup_method(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.analyzer = InheritanceAnalyzer(self.temp_dir)
    
    def teardown_method(self):
        """清理测试环境"""
        shutil.rmtree(self.temp_dir)
    
    def test_find_python_packages_empty(self):
        """测试空目录"""
        packages = self.analyzer.find_python_packages()
        assert packages == []
    
    def test_find_python_packages_single(self):
        """测试单个包"""
        # 创建包结构
        package_dir = Path(self.temp_dir) / "mypackage"
        package_dir.mkdir()
        (package_dir / "__init__.py").touch()
        
        packages = self.analyzer.find_python_packages()
        assert "mypackage" in packages
    
    def test_find_python_packages_nested(self):
        """测试嵌套包"""
        # 创建嵌套包结构
        package_dir = Path(self.temp_dir) / "mypackage"
        package_dir.mkdir()
        (package_dir / "__init__.py").touch()
        
        subpackage_dir = package_dir / "subpackage"
        subpackage_dir.mkdir()
        (subpackage_dir / "__init__.py").touch()
        
        packages = self.analyzer.find_python_packages()
        assert "mypackage" in packages
        assert "mypackage.subpackage" in packages
    
    def test_analyze_package_not_found(self):
        """测试分析不存在的包"""
        result = self.analyzer.analyze_package("nonexistent")
        assert "error" in result
    
    def test_analyze_package_empty(self):
        """测试分析空包"""
        # 创建空包
        package_dir = Path(self.temp_dir) / "emptypackage"
        package_dir.mkdir()
        (package_dir / "__init__.py").touch()
        
        result = self.analyzer.analyze_package("emptypackage")
        assert result["package_name"] == "emptypackage"
        assert result["modules"] == {}
        assert result["classes"] == {}
        assert result["inheritance_chains"] == {}
