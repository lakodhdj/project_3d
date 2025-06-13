from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import asyncpg.exceptions
from asyncpg import Connection
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password1@127.0.0.1:5432/printer_queue")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(2),
    retry=retry_if_exception_type((asyncpg.exceptions.ConnectionDoesNotExistError, asyncpg.exceptions.CannotConnectNowError)),
)
async def check_db_connection():
    logger.info("Attempting to connect to database at %s", DATABASE_URL)
    try:
        conn: Connection = await asyncpg.connect(DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://"))
        await conn.close()
        logger.info("Database connection successful")
    except Exception as e:
        logger.error("Database connection failed: %s", str(e))
        raise

async def init_db():
    await check_db_connection()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")

async def get_db():
    async with async_session() as session:
        yield session