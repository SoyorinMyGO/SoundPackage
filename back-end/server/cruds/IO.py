import json
from mailbox import FormatError
from pathlib import Path
import zipfile

from pydub import AudioSegment
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.Package import Package
from server.models.VoiceBelongPackage import VoiceBelongPackage
from server.models.Voice import Voice


# 导入语音文件
async def import_file_crud(position: str, db: AsyncSession) -> Voice | None:
    """导入语音文件

    Args:
        position(str): 要导入的文件路径
        db(AsyncSession): 数据库会话

    Returns:
        Voice: 是否导入成功
    """
    # 网络环境导入