from fastapi import APIRouter

from configs.db_config import get_db

router = APIRouter(prefix="/test", tags=['test'])

@router.get("/database")
async def get_database_session():
    try:
        get_db()
    except Exception as e:
        pass
    return f'数据库会话获取成功'