from enum import Enum

""" 角色枚举类型定义 """

class RoleEnum(Enum):
    """
    角色定义
    """
    admin = "admin" # 管理员
    landlord = "landlord"   # 房东
    tenant = "tenant"   # 租客


class OrderEnum(Enum):
    """
    订单状态
    """
    WAIT_PAY = "WAIT_PAY" # 待支付
    PAID = "PAID" # 已支付
    CANCELED = "CANCELED" # 已取消