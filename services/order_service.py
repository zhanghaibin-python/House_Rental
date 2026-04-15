from tortoise.transactions import atomic

from schemas.order import OrderCreateIn
from models.business import House, Order
from core.exceptions import BusinessException, ErrorCode
from core.enums import OrderEnum


class OrderService:

    @staticmethod
    @atomic()
    async def create_order(order_in: OrderCreateIn, user_id: int) -> dict:
        # 1. 查看房源是否存在，且是不是待租状态 (status=0)
        # select_for_update() 是企业级并发锁，防止多个人同时强一套房
        house = await (House.filter(id=order_in.house_id, status=0).
                       select_for_update().first())
        if not house:
            raise BusinessException(ErrorCode.HOUSE_RENTED_ERR)

        # 2. 后端安全计算总金额
        # 按每月 30 天算， 算出总天数，乘以 (月租/30)
        days = (order_in.end_date - order_in.begin_date).days
        if days < 0:
            raise BusinessException(ErrorCode.PARAM_ERR)    # 租期必须大于0天

        total_amount = round(float(house.price) / 30 * days, 2)

        # 3. 创建订单
        order = await Order.create(
            user_id=user_id,
            house_id=house.id,
            begin_date=order_in.begin_date,
            end_date=order_in.end_date,
            amount=total_amount,
            status="WAIT_PAY"
        )

        # 4. 把房源状态改为已租 (status=1)
        house.status = 1
        await house.save()

        return order.to_dict()

    @staticmethod
    async def mock_alipy_callback(order_id: int) -> bool:
        """ 模拟支付宝支付成功后的异步回调通知 """
        order = await Order.get_or_none(id=order_id)
        if not order:
            raise False

        if order.status.value == OrderEnum.WAIT_PAY.value:
            # 修改订单状态为已支付
            order.status = "PAID"
            await order.save()
        return True

