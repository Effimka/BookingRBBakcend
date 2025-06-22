from fastapi import FastAPI
from api import userAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Разрешить только указанные источники
    allow_credentials=True,
    allow_methods=["*"],            # Разрешить любые методы: GET, POST и т.д.
    allow_headers=["*"],            # Разрешить любые заголовки
)

@app.on_event("startup")
async def startup():
    print("Server started and wait POST-requests...")

app.include_router(userAPI.router)
