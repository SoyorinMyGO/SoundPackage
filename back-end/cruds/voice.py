from typing import Any, Sequence, Optional

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from models.Tag import Tag
from models.Voice import Voice
from models.VoiceBelongPackage import VoiceBelongPackage
from models.VoiceBelongTag import VoiceBelongTag


async def get_voice_list_crud(package_id: int, selected_tag_ids: Optional[list[int]] | None, db: AsyncSession) -> Sequence[Any]:
    """获取语音列表

    Args:
        package_id(int): 选择的语音包id
        selected_tag_ids(Optional[list[int]] | None): 选择的筛选词条
        db(AsyncSession): 数据库会话

    Returns:
        Sequence[Any]: 语音列表
    """
    # 创建语音包视图
    if package_id == 0:
        package_voice_subquery = select(Voice.id.label('voice_id')).subquery()

    else:
        package_voice_subquery = (
            select(VoiceBelongPackage.voice_id)
            .where(VoiceBelongPackage.package_id == package_id)
            .subquery()
        )

    if not selected_tag_ids:
        # 若没有选择标签，直接从视图中查询所有语音
        query = (
            select(Voice)
            .where(Voice.id.in_(select(package_voice_subquery.c.voice_id)))
            .order_by(Voice.used_times.desc(), Voice.created_at.desc())
        )
        result = await db.execute(query)
        return result.scalars().all()

    # 获取所有选中标签的path
    tag_query = select(Tag.id, Tag.path).where(Tag.id.in_(selected_tag_ids))
    tag_result = await db.execute(tag_query)
    tags = tag_result.all()

    if not tags:
        return []

    # 构建path匹配条件
    path_conditions = []
    for tag_id, path in tags:
        if path:
            # 匹配该标签及其所有子标签
            path_conditions.append(Tag.path.like(f"{path}%"))
        else:
            # 如果没有path，直接匹配ID
            path_conditions.append(Tag.id == tag_id)

    # 查询符合标签条件的语音
    # 先找出符合标签条件的语音ID
    tag_voice_query = (
        select(VoiceBelongTag.voice_id)
        .join(Tag, VoiceBelongTag.tag_id == Tag.id)
        .where(
            and_(
                VoiceBelongTag.voice_id.in_(select(package_voice_subquery.c.voice_id)),
                or_(*path_conditions)
            )
        )
        .distinct()
    )

    # 从Voice表中获取完整信息
    query = (
        select(Voice)
        .where(Voice.id.in_(tag_voice_query))
        .order_by(Voice.used_times.desc(), Voice.created_at.desc())
    )

    result = await db.execute(query)
    return result.scalars().all()