import hashlib
from pathlib import Path


def sha256_of_file(file: Path, chunk_size: int = 1024 * 1024):
    """获取文件的hash值

    Args:
        file(Path): 文件路径
        chunk_size(int): 一次读取的大小
    """
    h = hashlib.sha256()
    with open(file, 'rb') as f:
        while content := f.read(chunk_size):
            h.update(content)
    return h.hexdigest()