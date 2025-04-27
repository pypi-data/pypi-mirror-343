"""
SQLModel 模型相关工具
pip install sqlmodel
"""

from sqlmodel import SQLModel, Field

def get_model_fields(model:SQLModel):
    """
    获取模型所有字段
    """
    return getattr(model, "__fields__")

