from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from configs.db_config import get_db
from cruds import package
from utils.response import success_response

router = APIRouter(prefix="/api/package", tags=['package'])

@router.get("")
async def get_list_router(db: AsyncSession = Depends(get_db)):
    result = await package.get_list_crud(db)
    return success_response(message='获取语音包列表成功', data=result)

@router.post("")
async def add_package_router(name:str = Query(...,min_length=1, max_length=50, description='语音包名称'),
                             alias:Optional[str] = Query(None, min_length=1, max_length=50, description='语音包别称'),
                             db: AsyncSession = Depends(get_db)):
    new_package = await package.add_package_crud(name, db, alias)
    return success_response(message='添加语音包成功', data=new_package)