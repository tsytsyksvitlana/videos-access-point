import typing as t

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from web_app.config.settings import settings


class PostgresHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> t.AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


postgres_helper = PostgresHelper(
    url=settings.postgres.url,
    echo=settings.postgres.echo
)
