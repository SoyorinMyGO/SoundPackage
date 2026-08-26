from datetime import datetime
from typing import Optional

from sqlalchemy import Index, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Tag(Base):
    """
    标签ORM模型（使用物化路径）
    """
    __tablename__ = "tag"

    __table_args__ = (
        Index("idx_tag_path", "path"),  # 路径索引，支持层级查询
        Index("idx_tag_created_at", "created_at"),
        Index("idx_tag_updated_at", "updated_at"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment='标签id'
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment='标签名'
    )

    path: Mapped[Optional[str]] = mapped_column(
        String(500),
        default='',
        comment='物化路径，格式：/父id/子id/，用于快速查询所有子标签'
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        comment='标签创建时间'
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        comment='标签更新时间'
    )