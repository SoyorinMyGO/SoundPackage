from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/packages", tags=['packages'])

@router.get("")
async def get_list(db: AsyncSession):
    pass