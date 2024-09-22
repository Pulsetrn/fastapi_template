from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config.config import settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        # При использовании async взаимодействия с db все следующие за bind параметры
        # следует выключать и => управлять всеми данными вручную
        # т.е., если нужно сохранить изменения - используем await session.commit()
        # нужно получить свежие данные - await session.refresh()
        # Приведенные выше две команды полностью заменяют 3 параметра в sessionmaker
        # но их нжуно выполнять вручную, что и является основынм отличием
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_getter(self):
        async with self.session_factory() as session:
            yield session

    async def dispose(self):
        await self.engine.dispose()


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
