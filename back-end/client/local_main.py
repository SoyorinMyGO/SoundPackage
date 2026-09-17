from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from client.routers import IO
from client.utils.exception_handle import register_exception_handlers

app = FastAPI()
root_path = Path(__file__).resolve().parent.parent.parent  # 项目根目录路径
app.mount("/assets", StaticFiles(directory=root_path / "assets"), name="assets")

register_exception_handlers(app)

# 添加中间件
# noinspection bad-argument-type
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(IO.router)

if __name__ == '__main__':
    uvicorn.run("local_main:app", host="0.0.0.0", port=24999, reload=True)
