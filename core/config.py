from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    配置管理类
    Pydantic 会自动读取 .env 文件，把值赋给这些属性。
    如果 .env 没写，就会用这里的默认值
    """
    PROJECT_NAME: str = "房屋租赁系统"
    API_V1_STR: str = "/api/v1"

    # JWT 配置
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # 数据库配置
    DATABASE_URL: str

    # 告诉 pydantic 从哪个文件加载环境变量
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# 实例化配置对象。全局只需导入这个 settings
settings = Settings()