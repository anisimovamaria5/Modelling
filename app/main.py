from fastapi import FastAPI, Request
from app.api.v1.router import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello, Maria!'}

# Подключение роута
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для теста разрешите все домены (потом замените на фронтенд)
    allow_methods=["*"],
    allow_headers=["*"],
)
