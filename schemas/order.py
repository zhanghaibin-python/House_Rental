from pydantic import Field, BaseModel
from datetime import date


class OrderCreateIn(BaseModel):
    """ 前端创建订单时传的参数 """
    house_id: int = Field(..., description="要租的房源ID")
    begin_date: date = Field(..., description="起租日期")
    end_date: date = Field(..., description="退租日期")


class OrderItemOut(BaseModel):
    id: int
    house_id: int
    amount: float
    status: str
    begin_date: date
    end_date: date
    create_time_ts: int