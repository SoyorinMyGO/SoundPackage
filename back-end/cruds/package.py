from typing import Any, Sequence, Optional

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
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

async def add_package_crud(name: str, db: AsyncSession, alias: Optional[str] = None) -> Package:
    """新建语音包

    Args:
        name(str): 语音包名
        alias(str): 语音包别称
        db(AsyncSession): 数据库会话

    Returns:
        Package: 新建语音包的信息
    """
    package = Package(name=name, alias=alias)
    db.add(package)
    await db.commit()
    await db.refresh(package)

    return package