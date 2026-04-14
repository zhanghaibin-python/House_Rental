from typing import List

from pydantic import BaseModel, Field

class HouseCreateIn(BaseModel):
    """ 前端发布房源时传的参数 """
    title: str = Field(..., min_length=5, max_length=100, description="房源标题")
    price: float = Field(..., gt=0, description="月租金 (必须大于0)")
    area: int = Field(..., gt=0, description="面积 (平米)")
    address: str = Field(..., min_length=5, max_length=200, description="详细地址")


class HouseItemOut(BaseModel):
    """ 定义结构，为了 Swagger 生成文档 """
    id: int
    title: str
    price: float
    area: int
    address: str
    status: int
    owner_username: str
    create_time_ts: int


class HousePageOut(BaseModel):
    """ 分页响应结构 """
    total: int = Field(..., description="总记录数")
    items: List[HouseItemOut] = Field(..., description="当前页数据列表")