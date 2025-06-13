from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes import auth, printer, job

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Инициализация базы данных при старте
    yield
    # Код при остановке приложения, если нужен
    pass

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(printer.router)
app.include_router(job.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)