from typing import Optional

from pydantic import Field, BaseModel


# 修改语音包信息请求体
class PackageChangeRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description='更改后的语音包名')
    alias: Optional[str] = Field(None, min_length=1, max_length=50, description='更改后的别名')
