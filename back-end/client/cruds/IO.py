import json
from mailbox import FormatError
from pathlib import Path
import zipfile
from pydub import AudioSegment

from client.models.Voice import Voice


# 导入语音文件
# async def import_file_crud(position: str) -> Voice | None:
#     """导入语音文件
#
#     Args:
#         position(str): 要导入的文件路径
#
#     Returns:
#         Voice: 是否导入成功
#     """
#     # 本地导入
#     file = Path(position)
#     if file.exists():
#         # 当前路径对应为文件
#         if file.is_file():
#             # 读取文件元数据
#             audio = AudioSegment.from_file(file)
#             suffix = file.suffix
#             if suffix not in {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.webm', '.aac'}:
#                 raise FormatError
#             name = file.name
#             length = len(audio)
#             # 下载文件至本地
#             voice_root = Path(__file__).resolve().parent.parent.parent / 'assets' / 'voices'
#             dust = voice_root / name
#             print(dust)
#             with open(file, "rb") as fr, open(dust, 'wb') as fw:
#                 data = fr.read()
#                 fw.write(data)
#         else:
#             raise TypeError
#     # 若文件不存在
#     else:
#         raise FileNotFoundError
#     return None

# 导出语音包
async def export_package_crud(package_name:str, position: str, voice_list: list[Voice]) -> None:
    """导出语音包

    Args:
        package_name(str): 导出的语音包名
        voice_list(list[dics]): 要导出的语音列表各语音条目的信息
        position(str): 导出文件路径
    """
    if not voice_list:
        raise FileNotFoundError
    # 创建json数据字典
    file_path = Path(position)
    # 文件夹是否存在
    if file_path.exists():
        zip_file_path = file_path / f'{package_name}.zip'
        if Path(zip_file_path).exists():
            # 压缩文件是否已存在
            print(f"DEBUG(导出路径): {zip_file_path} 已存在")
            raise FileExistsError

        voice_data = []
        for item in voice_list:
            voice_data.append({'id': item.id, 'name': item.name})

        package_id = 0
        package_data = [{
            'id': package_id,
            'name': package_name,
            'len': len(voice_list),
            'voices': voice_data
        }]
        data_json = json.dumps(package_data, ensure_ascii=False)

        # 创建zip文件
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_STORED) as zip_file:
            for voice in voice_list:
                name = voice.name
                from local_main import root_path
                voice_path = root_path / 'assets' / 'voices' / name
                print(f'DEBUG(voice_path):${voice_path}')
                zip_file.write(voice_path, arcname=name)
            zip_file.writestr('data.json', data_json)
        return

    # 若导出路径不存在或不是文件夹
    raise NotADirectoryError