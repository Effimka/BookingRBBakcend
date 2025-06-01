from fastapi import FastAPI
from api import user

app = FastAPI()

@app.on_event("startup")
async def startup():
    print("Server started and wait POST-requests...")

app.include_router(user.router)