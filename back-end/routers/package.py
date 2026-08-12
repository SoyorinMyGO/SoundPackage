from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from configs.db_config import get_db
from cruds.package import get_list_crud
from utils.response import success_response

router = APIRouter(prefix="/api/package", tags=['package'])

@router.get("")
async def get_list_router(db: AsyncSession = Depends(get_db)):
    result = await get_list_crud(db)
    return success_response(message='获取语音包列表成功', data=result)