# SuperMro 快速开始指南 🚀

## 安装

### 方法1：直接安装（推荐）
```bash
# 克隆项目
git clone https://github.com/yourusername/supermro.git
cd supermro

# 运行安装脚本
python install.py
```

### 方法2：手动安装
```bash
# 安装依赖
pip install -r requirements.txt

# 安装SuperMro
pip install -e .
```

## 使用

### 基本用法

1. **进入您的Python项目目录**
   ```bash
   cd /path/to/your/python/project
   ```

2. **运行分析工具**
   ```bash
   # 交互式模式（推荐）
   python -m supermro
   
   # 或者直接指定包名
   python -m supermro --package your_package_name
   ```

### 高级用法

```bash
# 生成可视化图
python -m supermro --visualize

# 追踪方法定义
python -m supermro --trace

# 指定输出文件
python -m supermro --visualize --output my_inheritance.pdf

# 分析指定路径的项目
python -m supermro --project-path /path/to/project
```

## 示例

### 分析Django项目
```bash
cd /path/to/django/project
python -m supermro
```

### 分析Flask项目
```bash
cd /path/to/flask/project
python -m supermro --package myapp --visualize
```

### 分析任何Python包
```bash
cd /path/to/python/project
python -m supermro --package mypackage --visualize --trace
```

## 输出说明

### 控制台输出
- 📦 包信息
- 📁 模块信息
- 🧩 类继承关系
- ✅ 分析完成

### 可视化文件
- `{package_name}_inheritance.gv` - Graphviz源文件
- `{package_name}_inheritance.pdf` - PDF可视化图

## 故障排除

### 问题1：找不到包
```
❌ 未找到Python包，请确保当前目录包含Python包
```
**解决方案**：确保当前目录包含 `__init__.py` 文件

### 问题2：Graphviz未安装
```
⚠️ Graphviz 未安装，请运行: pip install graphviz
```
**解决方案**：
```bash
# macOS
brew install graphviz
pip install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz
pip install graphviz
```

### 问题3：模块导入失败
```
❌ 分析失败: 无法导入包 package_name
```
**解决方案**：检查包名是否正确，确保包可以正常导入

## 更多帮助

- 查看完整文档：`cat README.md`
- 查看帮助信息：`python -m supermro --help`
- 查看示例项目：`cd examples/sample_project`

---

**SuperMro** - 让Python继承关系分析变得简单！ 🧬
