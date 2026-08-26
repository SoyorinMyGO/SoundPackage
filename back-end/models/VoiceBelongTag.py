from datetime import datetime
from typing import Optional

from sqlalchemy import Index, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class VoiceBelongTag(Base):
    """
    语音归属标签关联表ORM模型
    """
    __tablename__ = "voice_belong_tag"

    __table_args__ = (
        Index("idx_vbt_tag_id", "tag_id"),
        Index("idx_vbt_voice_id", "voice_id"),
        Index("idx_vbt_tag_voice", "tag_id", "voice_id"),  # 复合索引，优化标签查询
        Index("idx_vbt_voice_tag", "voice_id", "tag_id"),  # 复合索引，优化语音查询
        UniqueConstraint("tag_id", "voice_id", name="uq_tag_voice"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment='关联记录id'
    )

    tag_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tag.id", ondelete="CASCADE"),
        nullable=False,
        comment='标签id'
    )

    voice_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("voice.id", ondelete="CASCADE"),
        nullable=False,
        comment='语音id'
    )