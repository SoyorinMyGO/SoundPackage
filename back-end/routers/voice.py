from fastapi import APIRouter, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db_config import get_db
from cruds import voice
from utils.response import success_response

router = APIRouter(prefix="/api/voice", tags=["voice"])

# 获取语音列表
@router.get("")
async def get_voice_list_router(db: AsyncSession = Depends(get_db)):
    data = await voice.get_voice_list_crud(db)
    return success_response(message='获取语音列表成功', data=data)

# 将语音批量导入同一语音包
@router.post("/{id}")
async def import_package(id: int = Path(..., description='语音id'),
                        db: AsyncSession = Depends(get_db)
):
    pass