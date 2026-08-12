from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.Package import Package

async def get_list_crud(db: AsyncSession) -> Sequence[Any]:
    """获取语音包列表
    Args:
        db(AsyncSession): 数据库会话

    Returns:
        Sequence[Any]: 语音包列表
    """
    query = select(Package).order_by(Package.updated_at)
    result = await db.execute(query)
    package_list = result.scalars().all()
    return package_list
