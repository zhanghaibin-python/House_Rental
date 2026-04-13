from datetime import datetime, timedelta
from typing import Any
import jwt

from core.config import settings

# 签名算法
ALGORITHM = "HS256"

def create_access_token(subject: str | Any, role: str = "tenant") -> str:
    """
    生成 JWT Token
    :param subject: user_id
    :param role: 用户角色，方便做权限控制
    :return: 返回签名
    """
    # 设置过期时间 (当前时间 + 120分钟)
    expire = datetime.utcnow() + timedelta(minutes=settings.
    ACCESS_TOKEN_EXPIRE_MINUTES)

    # payload 用于携带用户某些信息 (不能存放敏感信息)
    to_encode = {
        "exp": expire,  # 过期时间 (jwt 内置字段)
        "sub": str(subject),    # 主题标识 (通常存放 user_id)
        "role": role,   # 角色
    }

    # 使用配置里的 SECRET_KEY 和 HS256 算法进行签名
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    解析 JWT Token, 如果过期或被篡改，会抛出 PyJWTError
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithm=ALGORITHM)