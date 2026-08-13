from typing import Any, Sequence, Optional

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND

from models.Package import Package
from schemas.Package import PackageChangeRequest


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

async def change_package_crud(id: int, updated_data: PackageChangeRequest, db: AsyncSession) -> Package:
    """修改语音包信息

    Args:
        id(int): 语音包id
        updated_data(PackageChangeRequest): 修改信息数据
        db(AsyncSession): 数据库会话

    Returns:
        Package: 修改后语音包信息
    """
    # 更新重新赋值的数据
    data = updated_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )
    query = update(Package).where(Package.id == id).values(**data)
    result = await db.execute(query)
    print(f'DEBUG: UPDATE:{result}')

    # 检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='不存在的语音包')

    # 获取更新后的语音包信息
    query = select(Package).where(Package.id == id)
    result = await db.execute(query)
    package = result.scalar_one()
    print(f'DEBUG: package:{package}')

    return package