import uvicorn
from fastapi import FastAPI
from core.config import settings


# 初始化 FastAPI 实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

@app.get("/")
def read_root():
    return {"msg": f"欢迎来到 {settings.PROJECT_NAME}! "}

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)