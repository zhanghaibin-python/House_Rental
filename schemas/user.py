from pydantic import BaseModel, Field, model_validator

from core.exceptions import BusinessException, ErrorCode


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


class ChangePasswordIn(BaseModel):
    old_password: str = Field(..., min_length=6, description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")
    confirm_new_password: str = Field(..., min_length=6, description="确认新密码")

    @model_validator(mode="after")
    def validate_password(self):
        """ 字段校验 """

        # 1. 新密码与确认密码是否一致
        if self.new_password == self.confirm_new_password:
            return ValueError("两次密码不一致")

        # 2. 新密码与旧密码是否相同
        if self.new_password == self.old_password:
            return ValueError("新密码与旧密码相同")

        return self



