from email.policy import default

from tortoise import fields

from models.base import BaseModel
from core.enums import RoleEnum, OrderEnum


# ----------- 1. 用户表 ----------
class User(BaseModel):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True, description="用户名")
    password = fields.CharField(max_length=128, description="哈希密码")
    mobile = fields.CharField(max_length=11, null=True, description="手机号")
    # role 可以是 "admin", "landlord"(房东), "tenant"(租客)
    role = fields.CharEnumField(RoleEnum, default=RoleEnum.tenant, description="角色")

    class Meta:
        table = "user"


# ----------- 2. 房源表 ----------
class House(BaseModel):
    id = fields.IntField(pk=True)
    # 外键关联：发布房源的房东
    owner = fields.ForeignKeyField("models.User", related_name="houses", description="房东")

    title = fields.CharField(max_length=100, description="房源标题")
    price = fields.DecimalField(max_digits=10, decimal_places=2, description="月租金")
    area = fields.IntField(description="面接(平米)")
    address = fields.CharField(max_length=200, description="详细地址")

    status = fields.IntField(default=0, description="房屋状态")

    class Meta:
        table = "house"


# ----------- 3. 订单表 ----------
class Order(BaseModel):
    id = fields.IntField(pk=True)
    # 外键关联：租客是谁
    user = fields.ForeignKeyField("models.User", related_name="orders", description="下单租客")
    # 外键关联：租的哪个房子
    house = fields.ForeignKeyField("models.House", related_name="order_house", description="关联房源")

    begin_date = fields.DateField(description="起租日期")
    end_date = fields.DateField(description="退租日期")
    amount = fields.DecimalField(max_digits=10, decimal_places=2, description="订单总金额")

    status = fields.CharEnumField(OrderEnum, default=OrderEnum.WAIT_PAY, description="订单状态")

    class Meta:
        table = "order"

