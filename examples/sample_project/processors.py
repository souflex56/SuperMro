"""
数据处理器示例
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseProcessor(ABC):
    """基础处理器抽象类"""
    
    def __init__(self, name: str):
        self.name = name
        self.processed_count = 0
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """处理数据"""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """获取处理统计信息"""
        return {
            "name": self.name,
            "processed_count": self.processed_count
        }


class DataProcessor(BaseProcessor):
    """数据处理器"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name)
        self.config = config
    
    def process(self, data: Any) -> Any:
        """处理数据"""
        self.processed_count += 1
        print(f"Processing data with {self.name}: {data}")
        return data
    
    def validate(self, data: Any) -> bool:
        """验证数据"""
        return data is not None


class TextProcessor(DataProcessor):
    """文本处理器"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.encoding = config.get("encoding", "utf-8")
    
    def process(self, data: str) -> str:
        """处理文本数据"""
        self.processed_count += 1
        processed_text = data.strip().lower()
        print(f"Processing text with {self.name}: {processed_text}")
        return processed_text
    
    def extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        words = text.split()
        return [word for word in words if len(word) > 3]


class ImageProcessor(DataProcessor):
    """图像处理器"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.max_size = config.get("max_size", (1920, 1080))
    
    def process(self, data: Any) -> Any:
        """处理图像数据"""
        self.processed_count += 1
        print(f"Processing image with {self.name}: {data}")
        return data
    
    def resize(self, width: int, height: int):
        """调整图像大小"""
        print(f"Resizing image to {width}x{height}")
    
    def compress(self, quality: int = 80):
        """压缩图像"""
        print(f"Compressing image with quality {quality}")
