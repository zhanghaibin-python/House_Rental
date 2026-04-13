from tortoise import models, fields
from datetime import datetime


class BaseModel(models.Model):
    """
    全局数据库模型基类
    提供创建时间、更新时间，以及便捷的 to_dict 方法
    """

    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    def to_dict(self, exclude: list = None) -> dict:
        """
        对象转字典
        :param exclude: 想要剔除的字段名列表
        :return: 返回处理后的 json 字典
        """
        exclude = exclude or []
        data = {}
        for key, value in self.__dict__.items():
            if key.startswith("_") or key in exclude:
                continue

            # 将 datetime 对象转化为前端好用的时间戳
            if isinstance(value, datetime):
                data[f"{key}_ts"] = int(value.timestamp())
            else:
                data[key] = value

        return data

    class Meta:
        abstract = True # 抽象基类，不建表