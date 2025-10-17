# SuperMro 🧬- Python项目继承关系分析工具

自动扫描任意Python项目，分析类继承结构，生成可视化图表。
支持MRO分析、方法追踪、跨模块继承关系展示。

## ✨ 核心能力

- 🔍 **自动发现**：自动扫描Python包结构，分析模块中的类
- 📊 **继承分析**：分析完整的类继承关系和MRO（方法解析顺序）
- 🎨 **可视化**：生成美观的继承关系图
- 🔎 **方法追踪**：追踪方法在继承链中的定义位置
- 📁 **详细信息**：显示模块名、文件名、方法列表等
- 🚀 **即插即用**：在任何Python项目目录中直接运行

## 📊 效果展示

![继承关系分析示例](examples/eg.png)

*上图展示了SuperMro分析sample_project.processors模块生成的继承关系图：ImageProcessor和TextProcessor作为具体实现类，都继承自DataProcessor；DataProcessor继承自BaseProcessor抽象基类；BaseProcessor最终继承自Python的ABC（Abstract Base Class）。这种设计模式确保了所有处理器都遵循统一的接口规范，同时允许具体的子类实现各自特定的功能。图中每个类节点下方列出了该类的公共方法，如compress、get_stats、process等，帮助开发者快速了解类的功能接口。*

## 🚀 快速开始

### 安装

```bash
# 从源码安装
git clone https://github.com/yourusername/supermro.git
cd supermro
pip install -e .

# 或者直接安装依赖
pip install -r requirements.txt
```

### 使用

#### 方法1：交互式模式（推荐）

```bash
# 进入您的Python项目目录
cd /path/to/your/python/project

# 运行分析工具
python -m supermro
```

#### 方法2：命令行模式

```bash
# 分析当前目录
python -m supermro

# 分析指定包
python -m supermro --package myapp

# 生成可视化图
python -m supermro --visualize

# 追踪方法定义
python -m supermro --trace
```

#### 方法3：全局安装后使用

```bash
# 安装后可以在任何地方使用
pip install supermro
cd /path/to/your/python/project
supermro
```

## 📖 使用示例

### 示例1：分析Django项目

```bash
cd /path/to/django/project
python -m supermro
```

输出：
```
🚀 SuperMro - Python 继承关系分析工具
==================================================
🔍 发现 3 个包:
  1. myapp
  2. myapp.models
  3. myapp.views

请选择要分析的包 (1-3): 1

📦 开始分析包: myapp
============================================================

📁 模块: myapp.models (models.py)
🧩 类: User
   → User
   → AbstractUser
   → AbstractBaseUser
   → object

🧩 类: Post
   → Post
   → TimeStampedModel
   → object
```

### 示例2：生成可视化图

```bash
python -m supermro --visualize
```

生成的文件：
- `myapp_inheritance.gv` - Graphviz源文件
- `myapp_inheritance.pdf` - PDF可视化图

### 示例3：追踪方法定义

```bash
python -m supermro --trace
```

交互式输入：
```
请输入类名: User
请输入方法名: save
```

输出：
```
🔍 User.save() 调用顺序:
  🧭 User.save() 定义于 /path/to/myapp/models.py
  🧭 AbstractUser.save() 定义于 /path/to/django/contrib/auth/models.py
```

## 🎨 可视化特性

### 智能颜色分类
- 🔴 **红色系**：异常类 (`Exception`, `Error`)
- 🟢 **绿色系**：处理器类 (`Analyzer`, `Processor`)
- 🟠 **橙色系**：管理类 (`Config`, `Manager`)
- 🟣 **紫色系**：基础类 (`Enum`, `object`)
- ⚪ **灰色系**：其他类

### 详细信息显示
每个类节点包含：
- 类名
- 方法列表（前3个）
- 模块信息
- 文件信息

## 🛠️ 依赖要求

### 必需依赖
- Python 3.7+
- 标准库：`inspect`, `importlib`, `pkgutil`

### 可选依赖（用于可视化）
```bash
# 安装 Graphviz 系统软件
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# Windows
# 下载并安装 Graphviz: https://graphviz.org/download/

# 安装 Python 包
pip install graphviz
```

## 📁 项目结构

```
SuperMro/
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/
│   └── supermro/
│       ├── __init__.py
│       ├── analyzer.py      # 核心分析功能
│       ├── visualizer.py    # 可视化功能
│       └── cli.py          # 命令行接口
├── examples/               # 示例项目
├── tests/                  # 测试文件
└── docs/                   # 文档
```

## 🔧 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black src/
```

### 类型检查

```bash
mypy src/
```


**SuperMro** - 让Python继承关系分析变得简单！ 🚀
