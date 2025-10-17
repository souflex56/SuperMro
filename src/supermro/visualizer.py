#!/usr/bin/env python3
"""
继承关系可视化器

提供基于Graphviz的可视化功能，支持：
- 生成继承关系图
- 智能颜色分类
- 多种输出格式
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# 可选：安装 Graphviz 支持
try:
    from graphviz import Digraph
    HAS_GRAPHVIZ = True
except ImportError:
    HAS_GRAPHVIZ = False


class InheritanceVisualizer:
    """继承关系可视化器"""
    
    def __init__(self):
        """初始化可视化器"""
        self.has_graphviz = HAS_GRAPHVIZ
    
    def visualize_project_mro(self, analysis_result: Dict[str, Any], 
                            output_path: Optional[str] = None) -> Optional[str]:
        """
        可视化整个包的继承关系
        
        Args:
            analysis_result: 分析结果
            output_path: 输出路径，默认为包名
            
        Returns:
            生成的文件路径
        """
        if not self.has_graphviz:
            print("⚠️ Graphviz 未安装，请运行: pip install graphviz")
            return None
        
        package_name = analysis_result["package_name"]
        modules = analysis_result["modules"]
        
        if not modules:
            print("⚠️ 没有找到可分析的模块")
            return None
        
        # 创建图形
        dot = Digraph(
            comment=f"{package_name} Class Hierarchy",
            graph_attr={
                "rankdir": "TB",
                "nodesep": "0.3",
                "ranksep": "0.5",
                "splines": "ortho"
            }
        )
        
        # 按模块组织类
        module_classes = {}
        added_edges = set()
        
        # 收集数据
        for module_name, module_info in modules.items():
            file_name = module_info["file"]
            classes = []
            
            for class_name, class_info in module_info["classes"].items():
                methods = class_info["methods"]
                methods_str = ', '.join(methods[:3]) if methods else '无公共方法'
                if methods and len(methods) > 3:
                    methods_str += f'... (+{len(methods)-3})'
                
                classes.append({
                    'name': class_name,
                    'methods': methods_str,
                    'methods_count': len(methods)
                })
                
                # 收集继承关系
                mro = class_info["mro"][:-1]  # 去掉 object
                for i in range(len(mro)-1):
                    edge = (mro[i], mro[i+1])
                    if edge not in added_edges:
                        added_edges.add(edge)
            
            if classes:
                module_classes[module_name] = {
                    'file': file_name,
                    'classes': classes
                }
        
        # 创建模块集群
        self._create_module_clusters(dot, module_classes)
        
        # 添加继承关系边
        for child, parent in added_edges:
            dot.edge(child, parent, color="black", arrowhead="normal")
        
        # 生成文件
        if output_path is None:
            output_path = f"{package_name}_inheritance.gv"
        
        output_file = Path(output_path)
        dot.render(output_file, view=True)
        
        print(f"✅ 继承关系可视化生成成功: {output_file.absolute()}")
        return str(output_file.absolute())
    
    def _create_module_clusters(self, dot, module_classes: Dict[str, Any]):
        """创建模块集群"""
        module_names = list(module_classes.keys())
        
        for i, (module_name, module_data) in enumerate(module_classes.items()):
            file_name = module_data['file']
            classes = module_data['classes']
            
            # 确定模块类型和颜色
            cluster_color = self._get_module_color(module_name)
            
            # 创建 cluster
            with dot.subgraph(name=f'cluster_{i}') as cluster:
                # 设置 cluster 属性
                cluster.attr(label=f'{Path(module_name).name}\\n{file_name}\\n{len(classes)} 类')
                cluster.attr(style='filled,rounded')
                cluster.attr(color=cluster_color)
                cluster.attr(fontsize='12')
                cluster.attr(fontname='Arial')
                
                # 在 cluster 内添加类节点
                for class_info in classes:
                    self._create_class_node(cluster, class_info)
            
            # 添加强制垂直布局的不可见边
            if i < len(module_names) - 1:
                current_first_class = classes[0]['name'] if classes else None
                next_module_classes = module_classes[module_names[i + 1]]['classes']
                next_first_class = next_module_classes[0]['name'] if next_module_classes else None
                
                if current_first_class and next_first_class:
                    dot.edge(current_first_class, next_first_class, style="invis", weight="100")
    
    def _create_class_node(self, cluster, class_info: Dict[str, Any]):
        """创建类节点"""
        class_name = class_info['name']
        methods = class_info['methods']
        
        # 创建类节点标签
        if methods != '无公共方法':
            label = f'{class_name}\\n━━━━━━━━━━━━━━━━━━━━\\n• {methods}'
        else:
            label = f'{class_name}\\n━━━━━━━━━━━━━━━━━━━━\\n• {methods}'
        
        # 根据类的类型设置不同的颜色
        node_color = self._get_class_color(class_name)
        
        cluster.node(
            class_name, 
            label=label,
            shape="ellipse",
            fillcolor=node_color,
            style="filled,rounded",
            fontsize="10",
            fontname="Arial"
        )
    
    def _get_module_color(self, module_name: str) -> str:
        """获取模块颜色"""
        module_lower = module_name.lower()
        if 'exception' in module_lower or 'error' in module_lower:
            return "#ffebee"  # 红色系
        elif 'processor' in module_lower or 'analyzer' in module_lower:
            return "#e8f5e8"  # 绿色系
        elif 'config' in module_lower or 'manager' in module_lower:
            return "#fff3e0"  # 橙色系
        elif 'model' in module_lower or 'data' in module_lower:
            return "#e3f2fd"  # 蓝色系
        else:
            return "#f5f5f5"  # 灰色系
    
    def _get_class_color(self, class_name: str) -> str:
        """获取类颜色"""
        if 'Exception' in class_name or 'Error' in class_name:
            return "#ffcdd2"  # 浅红色
        elif 'Analyzer' in class_name or 'Processor' in class_name:
            return "#c8e6c9"  # 浅绿色
        elif 'Config' in class_name or 'Manager' in class_name:
            return "#ffe0b2"  # 浅橙色
        elif class_name in ['Enum', 'object']:
            return "#e1bee7"  # 浅紫色
        else:
            return "#f5f5f5"  # 浅灰色
