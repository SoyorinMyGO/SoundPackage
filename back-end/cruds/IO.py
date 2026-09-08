import json
from mailbox import FormatError
from pathlib import Path
import zipfile

from pydub import AudioSegment
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.Package import Package
from models.VoiceBelongPackage import VoiceBelongPackage
from models.Voice import Voice


# 导入语音文件
async def import_file_crud(position: str, db: AsyncSession) -> Voice | None:
    """导入语音文件

    Args:
        position(str): 要导入的文件路径
        db(AsyncSession): 数据库会话

    Returns:
        Voice: 是否导入成功
    """
    # 本地导入
    file = Path(position)
    if file.exists():
        # 当前路径对应为文件
        if file.is_file():
            # 读取文件元数据
            audio = AudioSegment.from_file(file)
            suffix = file.suffix
            if suffix not in {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.webm', '.aac'}:
                raise FormatError
            name = file.name
            length = len(audio)
            # 下载文件至本地
            voice_root = Path(__file__).resolve().parent.parent.parent / 'assets' / 'voices'
            dust = voice_root / name
            print(dust)
            with open(file, "rb") as fr, open(dust, 'wb') as fw:
                data = fr.read()
                fw.write(data)
            # 上传数据至数据库
            voice = Voice(name=name, length=length)
            db.add(voice)
            await db.commit()
            result = await db.refresh(voice)
            return result
    # 若文件不存在
    else:
        raise FileNotFoundError
    return None
    # 网络环境导入

# 导出语音包
async def export_file_crud(id: int, position: str, db: AsyncSession) -> None:
    """导出语音包

    Args:
        id(int): 语音包id
        position(str): 导出文件路径
        db(AsyncSession): 数据库会话
    """
    # 查询语音包信息
    # 若id为0(即选择的为所有语音)
    if id == 0:
        package_name = '全部语音'
        # 查询所有语音文件信息
        query = select(Voice.id, Voice.name).select_from(Voice)
        result = await db.execute(query)
        voice_list = result.all()
        if not voice_list:
            raise FileNotFoundError
    else:
        # 查询语音包名
        query = select(Package.name).where(Package.id == id)
        result = await db.execute(query)
        package_name = result.scalar_one_or_none()
        if not package_name:
            raise FileNotFoundError
        # 查询语音包下的语音文件信息
        query = select(Voice.id, Voice.name).select_from(Voice).join(VoiceBelongPackage, VoiceBelongPackage.voice_id == Voice.id).where(VoiceBelongPackage.package_id == id)
        result = await db.execute(query)
        voice_list = result.all()
        print(voice_list)
        if not voice_list:
            raise FileNotFoundError
    # 导出文件至指定位置
    direction = Path(position)
    if direction.exists() and direction.is_dir():
        # 创建压缩文件路径
        zip_file_path = direction / f'{package_name}.zip'
        print(f"DEBUG(导出路径): {zip_file_path}")
        if Path(zip_file_path).exists():
            print(f"DEBUG(导出路径): {zip_file_path} 已存在")
            raise FileExistsError
        # 创建json数据字典
        voice_data = []
        for item in voice_list:
            voice_data.append({'id': item.id, 'name': item.name})
        package_data = [{
            'id': id,
            'name': package_name,
            'len': len(voice_list),
            'voices': voice_data
        }]
        # 创建zip文件
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_STORED) as zip_file:
            for voice in voice_list:
                name = voice.name
                voice_path = Path(__file__).resolve().parent.parent.parent / 'assets' / 'voices' / name
                zip_file.write(voice_path, arcname=name)
            data_json = json.dumps(package_data, ensure_ascii=False)
            zip_file.writestr('data.json', data_json)
        return
    # 若导出路径不存在或不是文件夹
    raise NotADirectoryError