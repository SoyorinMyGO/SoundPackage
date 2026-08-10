import uvicorn
from fastapi import FastAPI
from routers import voice, test

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(voice.router)
app.include_router(test.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=24990, reload=True)
