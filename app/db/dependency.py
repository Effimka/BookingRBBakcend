from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import DATABASE_URL

# Создаем асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_recycle=3600,   # Переподключение каждый час
    pool_size=5,         # Размер пула соединений
    max_overflow=10      # Максимальное количество дополнительных соединений
)

# Создаем асинхронную фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Асинхронная функция для получения сессии
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()