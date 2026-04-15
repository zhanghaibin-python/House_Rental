from schemas.house import HouseCreateIn
from models.business import House, User
from core.exceptions import BusinessException, ErrorCode


class HouseService:
    @staticmethod
    async def publish(house_in: HouseCreateIn, owner_id: int) -> dict:
        """ 发布房源逻辑 """
        house = await House.create(
            owner_id=owner_id,
            title=house_in.title,
            price=house_in.price,
            area=house_in.area,
            address=house_in.address,
            status=0 # 默认待租
        )
        return house.to_dict()

    @staticmethod
    async def get_list(page: int, size: int) -> dict:
        """ 获取房源分页列表 (防御 N+1 查询) """
        # 1. 构造查询器：只查未下架的房源
        query = House.filter(status=0)

        # 2. 查总数 (用于分页)
        total = await query.count()

        # 3. 查当前页数据
        houses = await query.limit(size).offset((page - 1) * size).prefetch_related("owner")

        # 4. 数据扁平化处理
        items = []
        for h in houses:
            h_dict = h.to_dict()
            # 从查好的 owner 对象中直接提取名字
            h_dict["owner_username"] = h.owner.username
            items.append(h_dict)

        return {"total": total, "items": items}

    @staticmethod
    async def get_detail(house_id: int) -> dict:
        """ 获取房源详情 """
        house = await House.get_or_none(id=house_id).prefetch_related("owner")
        if not house:
            raise BusinessException(ErrorCode.HOUSE_NOT_FOUND_ERR)

        h_dict = house.to_dict()
        h_dict["owner_username"] = house.owner.username
        return h_dict
