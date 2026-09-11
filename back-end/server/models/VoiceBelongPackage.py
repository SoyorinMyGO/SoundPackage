from datetime import datetime
from typing import Optional

from sqlalchemy import Index, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class VoiceBelongPackage(Base):
    """
    语音归属语音包关联表ORM模型
    """
    __tablename__ = "voice_belong_package"

    __table_args__ = (
        Index("idx_vbp_voice_id", "voice_id"),
        Index("idx_vbp_package_id", "package_id"),
        Index("idx_vbp_package_voice", "package_id", "voice_id"),  # 复合索引，优化查询
        UniqueConstraint("voice_id", "package_id", name="uq_voice_package"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment='关联记录id'
    )

    voice_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("voice.id", ondelete="CASCADE"),
        nullable=False,
        comment='语音id'
    )

    package_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("package.id", ondelete="CASCADE"),
        nullable=False,
        comment='语音包id'
    )