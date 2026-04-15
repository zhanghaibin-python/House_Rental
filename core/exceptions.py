from enum import Enum


class ErrorCode(Enum):
    """ 全局错误码枚举 """
    SYSTEM_ERR = (5000, "系统繁忙，请稍后再试")
    PARAM_ERR = (4000, "参数校验错误")
    AUTH_ERR = (4001, "认证失败，请重新登录")
    ACCOUNT_EXIST_ERR = (4002, "账号已存在")
    USER_NOT_FOUND_ERR = (4003, "用户不存在或密码错误")
    NO_PERMISSION_ERR = (4004, "权限不足，拒绝访问")
    HOUSE_NOT_FOUND_ERR = (4005, "房源不存在")
    HOUSE_RENTED_ERR = (4006, "手慢了，该房源已被租走")
    ORDER_NOT_FOUND_ERR = (4007, "订单不存在")
    FILE_TYPE_ERR = (4008, "不支持的文件格式，仅允许上传图片")
    FILE_SIZE_ERR = (4009, "文件太大，超过了限制")
    NOT_FOUND_FILED = (4010, "未有可更新字段")



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