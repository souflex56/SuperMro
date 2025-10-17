"""
自定义异常示例
"""


class CustomError(Exception):
    """自定义基础异常"""
    
    def __init__(self, message: str, error_code: int = 0):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
    
    def __str__(self):
        return f"[{self.error_code}] {self.message}"


class ValidationError(CustomError):
    """验证错误"""
    
    def __init__(self, message: str, field: str = None):
        super().__init__(message, error_code=400)
        self.field = field
    
    def __str__(self):
        if self.field:
            return f"Validation error in field '{self.field}': {self.message}"
        return f"Validation error: {self.message}"


class ProcessingError(CustomError):
    """处理错误"""
    
    def __init__(self, message: str, processor_name: str = None):
        super().__init__(message, error_code=500)
        self.processor_name = processor_name
    
    def __str__(self):
        if self.processor_name:
            return f"Processing error in {self.processor_name}: {self.message}"
        return f"Processing error: {self.message}"


class DatabaseError(CustomError):
    """数据库错误"""
    
    def __init__(self, message: str, table: str = None):
        super().__init__(message, error_code=503)
        self.table = table
    
    def __str__(self):
        if self.table:
            return f"Database error in table '{self.table}': {self.message}"
        return f"Database error: {self.message}"
