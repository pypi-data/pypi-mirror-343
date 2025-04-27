"""
Amis Schemas
pip install pydantic
"""
from typing import Optional, Any, List
from pydantic import BaseModel


class BaseResponse(BaseModel):
    status:Optional[int] = 0
    msg:Optional[str] = None
    data:Optional[dict[str, Any]] = None


class TableData(BaseModel):
    """表格数据"""
    # 总数据量，用于生成分页
    total:Optional[int] = 0
    # 当前页码
    page:Optional[int] = 1
    # 每页显示的行数
    page_size:Optional[int] = 20
    # 是否有下一页
    hasNext:Optional[bool] = False
    # 行的数据
    items:Optional[List[Any]] = []

class TableResponse(BaseResponse):
    """表格响应"""
    data:TableData = []



