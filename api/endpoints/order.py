from fastapi import APIRouter, Depends

from schemas.order import OrderCreateIn
from models.business import User, Order
from api.deps import get_current_user
from services.order_service import OrderService
from core.response import success, fail
from core.exceptions import ErrorCode


router = APIRouter(prefix="/order", tags=["订单与支付模块"])


@router.post("/create", summary="创建租房订单")
async def create_order(order_in: OrderCreateIn, current_user: User = Depends(get_current_user)):
    """ 租房发起预定 """
    order_dict = await OrderService.create_order(order_in, current_user.id)
    return success(data=order_dict)

@router.get("/my", summary="查看我的订单列表")
async def get_my_orders(current_user: User = Depends(get_current_user)):
    """ 获取当前登录用户的所有订单列表 """
    orders = await Order.filter(user_id=current_user.id).order_by("-create_time")
    return success(data=[o.to_dict() for o in orders])

@router.post("/alipay/callback", summary="【模拟】支付宝支付成功回调")
async def alipay_callback(order_id: int):
    """
    此接口不需要鉴权
    这里模拟支付宝支付
    """
    is_success = await OrderService.mock_alipy_callback(order_id)
    if is_success:
        return success(msg="支付状态更新成功")
    return fail(code=ErrorCode.ORDER_NOT_FOUND_ERR.code, msg=ErrorCode.ORDER_NOT_FOUND_ERR.msg)