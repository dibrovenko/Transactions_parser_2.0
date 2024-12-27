import logging
from config.config import database_config

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


URL = (
    f"{database_config['type_db']}+{database_config['type_connect']}://"
    f"{database_config['user']}:{database_config['password']}@"
    f"{database_config['host']}:{database_config['port']}/"
    f"{database_config['db_name']}"
)

async_engine = create_async_engine(
    url=URL,
    echo=False,
)

async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
