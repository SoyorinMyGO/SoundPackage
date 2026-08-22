from mailbox import FormatError

from fastapi import APIRouter, Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from configs.db_config import get_db
from cruds import IO
from utils.response import success_response

router = APIRouter(prefix="/api/IO", tags=['io'])

# 导入语音包活语音文件
@router.post("/import/{position}")
async def import_file_router(position: str = Path(..., description='导入文件路径'),
                            db: AsyncSession = Depends(get_db)
):
    try:
        await IO.import_file_crud(position, db)
        success_response(message='文件导入成功', data=None)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='不存在的文件或文件夹')
    except FormatError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='不支持的文件格式')
