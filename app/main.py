import uvicorn

from fastapi import FastAPI
from app.api.routes.predict import router

app = FastAPI(title='ZypherAI')

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run (
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )