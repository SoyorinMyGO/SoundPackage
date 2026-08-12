from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/soundpackage?charset=utf8mb4"

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
            yield session   # 返回数据库
            await session.commit()  # 提交会话请求
        except Exception as e:
            await session.rollback()    # 回滚数据库
            raise Exception(f"无法获取数据库会话，错误信息:{e}")
        finally:
            await session.close()   # 关闭数据库会话