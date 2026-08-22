from fastapi import APIRouter, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db_config import get_db
from cruds import voice

router = APIRouter(prefix="/api/voice", tags=["voice"])

# 将语音批量导入同一语音包
@router.post("/{id}")
async def import_package(id: int = Path(..., description='语音id'),
                        db: AsyncSession = Depends(get_db)
):
    pass