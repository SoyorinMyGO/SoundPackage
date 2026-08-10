from fastapi import APIRouter

router = APIRouter(prefix="/api/voice", tags=["voice"])

# 将语音批量导入同一语音包
@router.post("/{id}")
async def import_package():
    pass