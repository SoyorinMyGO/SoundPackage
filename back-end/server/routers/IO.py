from mailbox import FormatError

from fastapi import APIRouter, Path, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from server.configs.db_config import get_db
from server.cruds import IO
from server.utils.response import success_response

router = APIRouter(prefix="/api/io", tags=['io'])

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

# 导出语音包
@router.post("/export/{id}")
async def export_file_router(id: int = Path(..., description='导出语音包id'),
                            position: str = Query(..., description='导出文件路径'),
                            db: AsyncSession = Depends(get_db)
):
    try:
        await IO.export_file_crud(id, position, db)
        success_response(message='语音包导出成功', data=None)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='不存在的语音包或空语音包')
    except NotADirectoryError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='导出路径不是文件夹')
    except FileExistsError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='压缩包已存在')
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='导出失败')