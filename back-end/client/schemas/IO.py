from pydantic import BaseModel, Field

from client.models.Voice import Voice


# 导出语音包请求体
class ExportPackageRequest(BaseModel):
    package_name: str = Field(..., description='语音包名称')
    position: str = Field(..., description='导出路径')
    voice_list: list[Voice] = Field(..., description='语音列表')