from typing import Optional

from fastapi import APIRouter, Depends, Query, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from configs.db_config import get_db
from cruds import package as crud
from utils.response import success_response
from schemas import Package as schemas

router = APIRouter(prefix="/api/package", tags=['package'])

@router.get("")
async def get_list_router(db: AsyncSession = Depends(get_db)
):
    result = await crud.get_list_crud(db)
    return success_response(message='获取语音包列表成功', data=result)

@router.post("")
async def add_package_router(name :str = Query(..., min_length=1, max_length=50, description='语音包名称'),
                             alias :Optional[str] = Query(None, min_length=1, max_length=50, description='语音包别称'),
                             db : AsyncSession = Depends(get_db)
):
    new_package = await crud.add_package_crud(name, db, alias)
    return success_response(message='添加语音包成功', data=new_package)

@router.post("/{id}")
async def change_package_router(
                                data: schemas.PackageChangeRequest,
                                id: int = Path(..., description='语音包id'),
                                db: AsyncSession = Depends(get_db)
):
    # 若包名和别名都没改变
    if data.name is None and data.alias is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='语音包名称与别名不能同时为空')
    result_package = await crud.change_package_crud(id,data, db)
    return success_response(message='更新语音包信息成功', data=result_package)

@router.delete("/{id}")
async def delete_package_router(id: int = Path(..., description='语音包id'),
                                db: AsyncSession = Depends(get_db)
):
    if not await crud.delete_package_crud(id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='不存在的语音包')
    return success_response(message='删除语音包成功', data=None)