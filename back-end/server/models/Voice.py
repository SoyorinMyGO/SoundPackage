from datetime import datetime
from typing import Optional

from sqlalchemy import Index, String, CheckConstraint, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Voice(Base):
    """
    语音ORM模型
    """
    __tablename__ = "voice"

    __table_args__ = (
        Index("idx_voice_created_at", "created_at"),
        Index("idx_voice_length", "length"),
        Index("idx_voice_used_times", "used_times"),
        CheckConstraint("length < 600000", name='check_length_less_than_600000')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='语音id')

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='语音名')

    length: Mapped[int] = mapped_column(Integer, nullable=False, comment='语音长度')

    used_times: Mapped[int] = mapped_column(Integer, default=0, comment='使用次数')

    hash_content: Mapped[str] = mapped_column(String(64), nullable=False, comment='语音哈希值')

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment='语音创建时间')

    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment='语音更新时间')
