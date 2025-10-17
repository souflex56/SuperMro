"""
数据模型示例
"""

from datetime import datetime
from typing import Optional, List


class BaseModel:
    """基础模型类"""
    
    def __init__(self, id: int):
        self.id = id
        self.created_at = datetime.now()
    
    def save(self):
        """保存模型"""
        print(f"Saving {self.__class__.__name__} with id {self.id}")
    
    def delete(self):
        """删除模型"""
        print(f"Deleting {self.__class__.__name__} with id {self.id}")


class User(BaseModel):
    """用户模型"""
    
    def __init__(self, id: int, username: str, email: str):
        super().__init__(id)
        self.username = username
        self.email = email
    
    def get_profile(self):
        """获取用户资料"""
        return {
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at
        }
    
    def change_password(self, new_password: str):
        """修改密码"""
        print(f"Changing password for user {self.username}")


class Post(BaseModel):
    """文章模型"""
    
    def __init__(self, id: int, title: str, content: str, author: User):
        super().__init__(id)
        self.title = title
        self.content = content
        self.author = author
        self.comments: List['Comment'] = []
    
    def add_comment(self, comment: 'Comment'):
        """添加评论"""
        self.comments.append(comment)
    
    def get_summary(self, max_length: int = 100) -> str:
        """获取文章摘要"""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."


class Comment(BaseModel):
    """评论模型"""
    
    def __init__(self, id: int, content: str, author: User, post: Post):
        super().__init__(id)
        self.content = content
        self.author = author
        self.post = post
    
    def edit(self, new_content: str):
        """编辑评论"""
        self.content = new_content
    
    def reply_to(self, parent_comment: 'Comment') -> 'Comment':
        """回复评论"""
        return Comment(
            id=self.id + 1000,  # 简单的ID生成
            content=f"回复 {parent_comment.author.username}: {self.content}",
            author=self.author,
            post=self.post
        )
