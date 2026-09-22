import json
from datetime import datetime
from os import mkdir
from pathlib import Path
import zipfile
from pydub import AudioSegment

from client.models.Voice import Voice
from client.schemas.IO import ImportFileResult, BatchImportPackageResponse
from client.utils.hash import sha256_of_file


# 导入语音文件
# noinspection bad-argument-type
async def import_files_crud(paths: list[str]) -> list[ImportFileResult] | None:
    """导入语音文件

    Args:
        paths(str): 要导入的文件路径

    Returns:
        Voice: 是否导入成功
    """
    # 本地导入
    results = []
    parsed = []
    for p in paths:
        file = Path(p)
        if not file.exists():
            results.append(ImportFileResult(path=p, status="failed", voice=None, error="文件不存在"))
            continue
        if not file.is_file():
            results.append(ImportFileResult(path=p, status="failed", voice=None, error="不是文件"))
            continue
        suffix = file.suffix.lower()
        if suffix not in {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.webm', '.aac'}:
            results.append(ImportFileResult(path=p, status="failed", voice=None, error="不支持的格式"))
            continue
        parsed.append((p, file))

    hashes = {}
    for p, file in parsed:
        try:
            # 获取文件hash值
            h = sha256_of_file(file)
            # 读取文件元数据
            audio = AudioSegment.from_file(file)
            length = len(audio)
            hashes[h] = {
                "path": p,
                "file": file,
                "hash": h,
                "length": length,
                "name": file.name
            }
        except Exception as e:
            results.append(ImportFileResult(path=p, status="failed", voice=None, error=str(e)))

    for h, info in hashes.items():
        voice = Voice(
            id=None,
            remote_id=None,
            name=info["name"],
            alias=None,
            length=info["length"],
            used_times=0,
            hash_content=h,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        # 转移文件
        # 检查父文件夹是否存在
        from client.local_main import root_path
        voice_root = root_path / "assets/voices"
        if not Path(voice_root).exists():
            mkdir(voice_root)

        suffix = Path(info["path"]).suffix.lower()
        dust = voice_root / f"{voice.hash_content}{suffix}"
        if Path(dust).exists():
            # 若出现hash值相同的文件
            results.append(ImportFileResult(path=info["path"], status="failed", voice=None, error="文件已存在"))
            continue
        with open(info["path"], "rb") as fr, open(dust, 'wb') as fw:
            while data := fr.read(1024 * 1024):
                fw.write(data)
        results.append(ImportFileResult(path=info["path"], status="success", voice=voice))
    return results

# 导入语音包
async def import_package_crud(path: str) -> BatchImportPackageResponse | None:
    """导入语音包

    Args:
        path(str): 被导入语音包的压缩文件路径
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError
    # 解压文件
    from client.local_main import root_path
    dust = root_path / 'assets/voices'
    with zipfile.ZipFile(file_path, "r") as zf:
        for file_info in zf.infolist():
            if file_info.filename.endswith(".json"):
                # 读取数据
                with zf.open(file_info) as f:
                    data_json = json.load(f)
                continue

            zf.extract(file_info, dust)
    # 解析数据
    data = data_json[0]
    package_name = data['name']
    voice_list = []
    for item in data['voices']:
        voice = Voice(remote_id=item['remote_id'], name=item['name'], alias=item['alias'], hash_content=item['hash_content'], length=item['length'])
        voice_list.append(voice)

    return BatchImportPackageResponse(package_name=package_name, result=voice_list)

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
            voice_data.append({"remote_id": item.remote_id, "name": item.name, "alias": item.alias, "hash_content": item.hash_content, "length": item.length})

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
                suffix = '.' + (voice.name.split('.')[-1] or '').lower()
                if not suffix or suffix == '.':
                    suffix = '.wav'
                name = voice.hash_content + suffix
                from client.local_main import root_path
                voice_path = root_path / 'assets' / 'voices' / name
                print(f'DEBUG(voice_path):${voice_path}')
                zip_file.write(voice_path, arcname=name)
            zip_file.writestr('data.json', data_json)
        return

    # 若导出路径不存在或不是文件夹
    raise NotADirectoryError