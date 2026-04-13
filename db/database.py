from tortoise import Tortoise
from core.config import settings


async def init_db():
    """
    初始化数据库连接并自动建表
    """
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={
            "models": ["models.business"]
        }
    )
    await Tortoise.generate_schemas()
    print("数据库连接成功，表结构已同步! ")

async def close_db():
    """
    断开数据库连接
    """
    await Tortoise.close_connections()
    print("数据库连接已断开! ")
