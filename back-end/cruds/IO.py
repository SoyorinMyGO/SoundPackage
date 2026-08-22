import os
from mailbox import FormatError
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

# 导入语音包或语音文件
async def import_files_crud(position: str, db: AsyncSession) -> bool | None:
    """导入语音包或语音文件

    Args:
        position(str): 要导入的文件路径
        db(AsyncSession): 数据库会话

    Returns:
        bool: 是否导入成功
    """
    # 本地导入
    file = Path(position)
    if file.exists():
        # 当前路径对应为文件
        if file.is_file():
            # 读取文件元数据
            suffix = file.suffix
            if suffix not in {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.webm'}:
                raise FormatError
            name = file.name
            # 下载文件至本地
            voice_root = Path(__file__).resolve().parent.parent.parent / 'assets' / 'voices'
            dust = voice_root / name
            print(dust)
            with open(file, "rb") as fr, open(dust, 'wb') as fw:
                data = fr.read()
                fw.write(data)
            return True
        # 当前路径对应为文件夹
        else:
            pass
    # 若文件不存在
    else:
        raise FileNotFoundError
    # 网络环境导入

