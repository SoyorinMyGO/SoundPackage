from typing import Any, Sequence

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from models.Voice import Voice


async def get_voice_list_crud(db: AsyncSession) -> Sequence[Any]:
    """获取语音列表

    Args:
        db(AsyncSession): 数据库会话

    Returns:
        Sequence[Any]: 语音列表
    """
    query = select(Voice).order_by(desc(Voice.used_times)).order_by(desc(Voice.updated_at))
    result = await db.execute(query)
    voice_list = result.scalars().all()
    return voice_list