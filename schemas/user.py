from pydantic import BaseModel, Field

class UserRegisterIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    password: str = Field(..., min_length=6, description="密码")
    mobile: str | None = Field(default=None, pattern=r"^1[3-9]\d{9}$",
                               description="手机号")
    role: str = Field(default="tenant", description="角色")


class UserLoginIn(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserUpdateIn(BaseModel):
    username: str | None = Field(default=None, description="用户名")
    mobile: str | None = Field(default=None, pattern=r"^1[3-9]\d{9}$", description="手机号")