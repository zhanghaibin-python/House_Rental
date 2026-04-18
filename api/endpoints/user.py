from fastapi import APIRouter, Depends

from schemas.user import UserRegisterIn, UserLoginIn, UserUpdateIn, ChangePasswordIn
from services.user_service import UserService
from core.response import success
from models.business import User
from api.deps import get_current_user


router = APIRouter(prefix="/user", tags=["用户模块"])

@router.post("/register", summary="用户注册")
async def register(user_in: UserRegisterIn):
    user_dict = await UserService.register(user_in)
    return success(data=user_dict)

@router.post("/login", summary="用户登录")
async def login(user_in: UserLoginIn):
    token_info = await UserService.login(user_in)
    return success(data=token_info)

@router.get("/me", summary="获取当前用户信息")
async def get_me(current_user: User = Depends(get_current_user)):
    """
    请求时必须携带 Authorization: Bearer <token> 才能访问
    :return:
    """
    return success(data=current_user.to_dict(exclude=["password"]))

@router.put("/update", summary="更新用户信息")
async def update_user(user_in: UserUpdateIn, current_user: User = Depends(get_current_user)):
    """
    更新用户信息
    """
    await UserService.update_user(current_user.id, user_in)
    return success(data=current_user.to_dict(exclude=["password"]))


@router.put("/change_password", summary="密码修改模块")
async def change_password(password_in: ChangePasswordIn, current_user: User = Depends(get_current_user)):
    """ 更改用户密码 """
    await UserService.change_password(current_user.id, password_in)
    return success(data=current_user.to_dict(exclude=["password"]))

