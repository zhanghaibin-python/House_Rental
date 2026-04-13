from enum import Enum


class ErrorCode(Enum):
    """ 全局错误码枚举 """
    SYSTEM_ERR = (5000, "系统繁忙，请稍后再试")
    PARAM_ERR = (4000, "参数校验错误")
    AUTH_ERR = (4001, "认证失败，请重新登录")
    ACCOUNT_EXIST_ERR = (4002, "账号已存在")
    USER_NOT_FOUND_ERR = (4003, "用户不存在或密码错误")

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg


class BusinessException(Exception):
    """
    全局业务异常类
    只要是 raise BusinessException, 就会被拦截器
    全局拦截返回给前端
    """
    def __init__(self, error_code: ErrorCode):
        self.code = error_code.code
        self.msg = error_code.msg