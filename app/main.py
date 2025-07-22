from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from routes import auth, printer, job, material
from dependencies import close_redis
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Инициализация базы данных при старте
    yield
    await close_redis()
app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(printer.router)
app.include_router(job.router)
app.include_router(material.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)