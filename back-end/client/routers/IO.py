from fastapi import APIRouter, HTTPException, Query
from starlette import status

from client.cruds import IO
from client.schemas.IO import ExportPackageRequest, ImportFileRequest
from client.utils.response import success_response

router = APIRouter(prefix="/api/io", tags=['io'])

# 导入语音文件
@router.post("/import/file")
async def import_file_router(data: ImportFileRequest):
    result = await IO.import_files_crud(data.paths)
    return success_response(message='文件导入成功', data=result)

# 导入语音包
@router.post("/import/package")
async def import_package_router(path: str = Query(..., description="被导入语音包的路径")):
    try:
        result = await IO.import_package_crud(path)
        return success_response(message='导入语音包成功', data=result)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='文件不存在')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='导入失败')

# 导出语音包
@router.post("/export")
async def export_package_router(data: ExportPackageRequest):
    try:
        await IO.export_package_crud(data.package_name, data.position, data.voice_list)
        return success_response(message='语音包导出成功', data=None)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='不存在的语音包或空语音包')
    except NotADirectoryError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='导出路径不是文件夹')
    except FileExistsError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='压缩包已存在')
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='导出失败')