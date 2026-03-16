from fastapi import FastAPI
from app.api.chat import router
from app.services.rag_service import init_knowledge
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_knowledge()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api") # 建议加个前缀，更规范

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

# 在 app.include_router 之后添加
for route in app.routes:
    print(f"DEBUG: 注册路由: {route.path}")