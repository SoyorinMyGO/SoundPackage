from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Package(Base):
    """
    语音包ORM模型
    """
    __tablename__ = 'package'

    __table_args__ = (
        Index('idx_package_updated_at', "updated_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='语音包id')
    name: Mapped[str] = mapped_column(String, unique=True, nullable=True, comment='语音包名')
    alias: Mapped[str] = mapped_column(String, comment='别名')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment='更新时间')

    def __repr__(self) -> str:
        return f'<Package(id={self.id}, name={self.name}, alias={self.alias}, created_at={self.created_at}, updated_at={self.updated_at})'