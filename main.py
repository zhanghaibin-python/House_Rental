from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request

from core.config import settings
from core.exceptions import BusinessException
from core.response import fail, success
from core.exceptions import ErrorCode
from db.database import init_db, close_db
from models.business import User
from api.deps import get_current_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    await init_db()
    yield
    # 关闭时执行
    await close_db()

# 初始化 FastAPI 实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# ------------------ 全局异常拦截器挂载 ---------------------
@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    """ 拦截业务异常 (如密码错误、账号已存在) """
    print(f"[业务异常] {request.url} - {exc.code}: {exc.msg}")
    return fail(code=exc.code, msg=exc.msg)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """ 拦截 Pydantic 的参数校验错误（如手机号格式错误） 替换 FastAPI 默认的422 """
    # 提取具体的报错字段和信息
    errors = exc.errors()
    error_msg = "; ".join([f"{'.'.join(str(x) for x in e['loc'])}: {e['msg']}" for e in errors])
    print(f"[参数异常] {request.url} - {error_msg}")

    return fail(code=ErrorCode.PARAM_ERR.code, msg=f"{ErrorCode.PARAM_ERR.msg}: {error_msg}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """ 兜底拦截未知大错（如 1/0，数据库连不上） """
    print(f"[系统崩溃] {request.url} - {str(exc)}")
    return fail(code=ErrorCode.SYSTEM_ERR.code, msg=ErrorCode.SYSTEM_ERR.msg)


@app.get("/")
def read_root():
    return {"msg": f"欢迎来到 {settings.PROJECT_NAME}! "}

@app.get("/test-error")
async def test_error(type: str):
    if type == "biz":
        raise BusinessException(ErrorCode.ACCOUNT_EXIST_ERR)
    elif type == "sys":
        return 1 / 0
    return  success()

@app.get("/test-auth")
async def test_auth(current_user: User = Depends(get_current_user)):
    """
    测试鉴权接口
    只有在请求头里带了合法 Token 的用户才能进来
    :param current_user:
    :return:
    """
    # 当进入这个函数时，current_user 已经从数据库查到了真实对象
    # Depends(get_current_user) 已经完成了用户合法校验
    return success(data={
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
    })


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)