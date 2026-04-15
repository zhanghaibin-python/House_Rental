from fastapi import APIRouter, UploadFile, File, Depends

from models.business import User
from api.deps import get_current_user
from services.upload_service import UploadService
from core.response import success


router = APIRouter(prefix="/upload", tags=["文件上传模块"])

@router.post("/image", summary="上传图片")
async def upload_image(
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user)
):
    """
    必须登录才能上传文件 (防止被当成免费图床)
    """
    img_url = await UploadService.upload_image(file)
    return success(data={"url": img_url})