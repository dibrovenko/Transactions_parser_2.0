import datetime
import enum
from sqlalchemy import create_engine, Column, String, Float, DateTime, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
from uuid import uuid4, UUID

from db.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]


class TypeTransactionEnum(enum.Enum):
    create = "create"
    sell = "sell"
    buy = "buy"


class TransactionSQLAlchemy(Base):
    __tablename__ = "transactions"

    id: Mapped[intpk]
    signature: Mapped[str] = mapped_column(String, nullable=False)
    mint: Mapped[str] = mapped_column(String, nullable=False)
    traderPublicKey: Mapped[str] = mapped_column(String, nullable=False)
    txType: Mapped[TypeTransactionEnum] = mapped_column(Enum(TypeTransactionEnum), nullable=False)
    solAmount: Mapped[float] = mapped_column(Float, nullable=False)

    tokenAmount: Mapped[float | None] = mapped_column(Float, nullable=True)
    initialBuy: Mapped[float | None] = mapped_column(Float, nullable=True)
    bondingCurveKey: Mapped[str | None] = mapped_column(String, nullable=True)
    newTokenBalance: Mapped[float | None] = mapped_column(Float, nullable=True)
    vTokensInBondingCurve: Mapped[float | None] = mapped_column(Float, nullable=True)
    vSolInBondingCurve: Mapped[float | None] = mapped_column(Float, nullable=True)
    marketCapSol: Mapped[float | None] = mapped_column(Float, nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    symbol: Mapped[str | None] = mapped_column(String, nullable=True)
    uri: Mapped[str | None] = mapped_column(String, nullable=True)
    pool: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Добавляем индекс на поле created_at
    __table_args__ = (
        Index('idx_created_at', 'created_at'),  # Имя индекса и колонка
    )
    """
        Что происходит с индексом?
            Индекс — это специальная структура данных, аналогичная сортированному указателю на строки таблицы.
            Когда добавляется индекс на поле created_at, база данных строит B-дерево или хэш-таблицу для быстрого поиска.
            При запросе база данных ищет не в основной таблице, а в индексе (как по оглавлению в книге).
            Это позволяет найти нужные строки за миллисекунды, независимо от размера таблицы.
    """
