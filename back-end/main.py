import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import voice, test, package, IO
from utils.exception_handle import register_exception_handlers

app = FastAPI()

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

app.include_router(voice.router)
app.include_router(test.router)
app.include_router(package.router)
app.include_router(IO.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=24990, reload=True)
