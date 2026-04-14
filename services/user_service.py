from passlib.context import CryptContext


from schemas.user import UserRegisterIn, UserLoginIn
from models.business import User
from core.exceptions import BusinessException, ErrorCode
from core.security import create_access_token


# 配置 bcrypt 加密算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    async def register(user_in: UserRegisterIn) -> dict:
        """ 注册逻辑 """
        # 1. 检查用户名是否存在
        if await User.filter(username=user_in.username).exists():
            raise BusinessException(ErrorCode.AUTH_ERR)

        # 密码加密
        hashed_password = pwd_context.hash(user_in.password)

        # 存入数据库
        new_user = await User.create(
            username=user_in.username,
            password=hashed_password,
            mobile=user_in.mobile,
            role=user_in.role,
        )

        # 返回删除了密码的字典
        return new_user.to_dict(exclude=['password'])


    @staticmethod
    async def login(user_in: UserLoginIn) -> dict:
        """ 登录逻辑 """
        # 1.查出用户
        user = await User.filter(username=user_in.username).first()
        if not user:
            raise BusinessException(ErrorCode.USER_NOT_FOUND_ERR)

        # 校验密码
        if not pwd_context.verify(user_in.password, user.password):
            raise BusinessException(ErrorCode.USER_NOT_FOUND_ERR)

        # 3. 签发JWT Token
        token = create_access_token(subject=user.id, role=user.role.value)

        # 返回 Token (符合 OAuth2 标准的结构)
        return {
            "access_token": token,
            "token_type": "bearer",
        }


