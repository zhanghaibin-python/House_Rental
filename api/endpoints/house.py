from fastapi import APIRouter, Depends, Query

from models.business import User
from schemas.house import HouseCreateIn
from api.deps import get_current_user
from core.exceptions import BusinessException, ErrorCode
from services.house_service import HouseService
from core.response import success


router = APIRouter(prefix="/house", tags=["房源模块"])


async def require_landlord(current_user: User = Depends(get_current_user)) -> User:
    """
    复合依赖：先过 get_current_user（必须登录），在检查 role (必须是房东)
    :param current_user:
    :return:
    """
    if current_user.role.value != "landlord":
        raise BusinessException(ErrorCode.NO_PERMISSION_ERR)
    return current_user


@router.post("/publish", summary="发布房源")
async def publish(house_in: HouseCreateIn, landlord: User = Depends(require_landlord)):
    """
    确保只有 房东才能进门，其它直接被拦截
    """
    house_dict = await HouseService.publish(house_in, landlord.id)
    return success(data=house_dict)


@router.get("/list", summary="分页获取房源列表")
async def get_list(
        page: int = Query(1, ge=1, description="页码"),
        size: int = Query(10, ge=1, le=100, description="每页数量")
):
    """
    这个接口允许任何人访问，且是公开的。
    Query(ge=1) 是 FastAPI 提供的校验，防止有人传 page=-1 导致 SQL 报错
    """
    page_data = await HouseService.get_list(page, size)
    return success(data=page_data)

@router.get("/{house_id}", summary="获取房源详情")
async def get_detail(house_id: int):
    house_dict = await HouseService.get_detail(house_id)
    return success(data=house_dict)