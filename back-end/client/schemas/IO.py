from pydantic import BaseModel, Field

from client.models.Voice import Voice


# 导出语音包请求体
class ExportPackageRequest(BaseModel):
    package_name: str = Field(..., description='语音包名称')
    position: str = Field(..., description='导出路径')
    voice_list: list[Voice] = Field(..., description='语音列表')

# 导入语音请求体
class ImportFileRequest(BaseModel):
    paths: list[str] = Field(..., description='被导入语音的路径列表')

# 导入语音响应体
class ImportFileResult(BaseModel):
    path: str
    status: str
    voice: Voice | None
    error: str | None = None

class BatchImportResponse(BaseModel):
    reslut: list[ImportFileResult]