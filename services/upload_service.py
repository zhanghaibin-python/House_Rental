import os
import uuid
import aiofiles
from fastapi import UploadFile

from core.exceptions import BusinessException, ErrorCode

# 本地存储目录
UPLOAD_DIR = "static/images"
# 确保目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 允许上传的图片格式
ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif", "webp"
}


class UploadService:

    @staticmethod
    async def upload_image(file: UploadFile):
        """ 处理图片上传，返回可访问的 URL """

        # 1. 提取后缀并校验文件类型
        ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
        if ext not in ALLOWED_EXTENSIONS:
            raise BusinessException(ErrorCode.FILE_TYPE_ERR)

        # 2. 防碰撞：使用 UUID 生成全球唯一文件名 (不用用户原文件名，防止乱码和黑客注入)
        new_filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, new_filename)

        # 3. 限制文件大小为 5MB (防止恶意塞满硬盘)
        MAX_SIZE = 5 * 1024 *1024

        # 4. 使用 aiofiles 异步分块写入磁盘，绝不阻塞主线程
        async with aiofiles.open(filepath, 'wb') as out_file:
            content = await file.read() # 读取内容
            if len(content) > MAX_SIZE:
                raise BusinessException(ErrorCode.FILE_SIZE_ERR)
            await out_file.write(content)

        # 在真实的七牛云场景中，这里应该是：
        # return await loop.run_in_executor(executor, qiniu.put_data, token, key, content)

        # 5. 返回路径 URL , 且是相对路径
        return f"/static/images/{new_filename}"

