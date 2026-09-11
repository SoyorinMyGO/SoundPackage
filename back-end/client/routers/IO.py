from mailbox import FormatError

from fastapi import APIRouter, Path, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from client.cruds import IO
from client.schemas.IO import ExportPackageRequest
from client.utils.response import success_response

router = APIRouter(prefix="/api/io", tags=['io'])

# 导入语音文件
@router.post("/import/file/{position}")
async def import_file_router(position: str = Path(..., description='导入文件路径')
):
    try:
        await IO.import_file_crud(position)
        success_response(message='文件导入成功', data=None)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='不存在的文件或文件夹')
    except FormatError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='不支持的文件格式')

# 导出语音包
@router.post("/export")
async def export_package_router(data: ExportPackageRequest):
    try:
        await IO.export_package_crud(data.package_name, data.position, data.voice_list)
        success_response(message='语音包导出成功', data=None)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='不存在的语音包或空语音包')
    except NotADirectoryError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='导出路径不是文件夹')
    except FileExistsError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='压缩包已存在')
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='导出失败')