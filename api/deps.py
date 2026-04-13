from fastapi import Header, Depends
import jwt

from core.exceptions import BusinessException, ErrorCode
from models.business import User
from core.security import decode_access_token


async def get_token_from_header(authorization:str = Header(None)) -> str:
    """
    从请求头中提取 Token. 前端通常发：Authorization: Bearer <Token>
    :param authorization:
    :return:
    """
    if not authorization or not authorization.startswith('Bearer '):
        raise BusinessException(ErrorCode.AUTH_ERR)
    # 截取 "Bearer " 后面的真实 token
    return authorization.split(" ")[1]


async def get_current_user(token: str = Depends(get_token_from_header)) -> User:
    """
    FastAPI 依赖注入函数：获取当前登录用户
    :param token:
    :return:
    """
    try:
        # 1. 解密 token
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise BusinessException(ErrorCode.AUTH_ERR)
    except jwt.PyJWTError:
        # Token 过期或被人伪造了
        raise BusinessException(ErrorCode.AUTH_ERR)

    # 2. 取数据库里查这个用户是否存在
    # (可能注销了账号，但手里还有未过期的 Token)
    user = await User.get_or_none(id=int(user_id))
    if not user:
        raise BusinessException(ErrorCode.AUTH_ERR)

    # 把 orm 对象返回给路由函数
    return user
