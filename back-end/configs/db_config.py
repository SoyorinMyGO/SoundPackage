from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import logging

ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/soundpackage?charset=utf8mb4"

logger = logging.getLogger(__name__)

# 创建数据库引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL, # 数据库URL
    echo=True,
    pool_size=10,   # 池容量
    max_overflow=20,    # 最大溢出容量
)

# 创建会话工厂
async_session_local = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    """获取数据库会话"""
    async with async_session_local() as session:
        try:
            yield session
            await session.commit()  # 如果没有异常，提交事务
        except HTTPException:
            # HTTP 业务异常，直接抛出
            await session.rollback()
            raise
        except SQLAlchemyError as e:
            # 数据库异常
            await session.rollback()
            logger.error(f"数据库错误: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"数据库操作失败: {str(e)}"
            )
        except Exception as e:
            # 其他未知异常
            await session.rollback()
            logger.error(f"未知错误: {e}")
            raise HTTPException(
                status_code=500,
                detail="服务器内部错误"
            )
        finally:
            await session.close()