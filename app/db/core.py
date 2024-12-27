import logging
import os
import shutil
import json
import traceback
from typing import List, Type, Literal

from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text, desc
from datetime import datetime, timedelta


from config import setup_logger
from db.database import Base, async_engine, async_session_factory
from db.models import TransactionSQLAlchemy
from db.schemas import TransactionDTO


logger = setup_logger(name=__name__, log_file=__name__, level=logging.INFO)


class AsyncORM:

    @staticmethod
    async def create_tables(flag: Literal['delete', 'restart']):
        if flag == "delete":
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

        elif flag == "restart":
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        else:
            raise ValueError("Недопустимое значение аргумента")

    @staticmethod
    async def insert_list_to_db(list_class_sqlalchemy: List[TransactionSQLAlchemy]):
        try:
            async with async_session_factory() as session:
                session.add_all(list_class_sqlalchemy)
                await session.commit()

        except Exception as e:
            print(e)
            logger.error(f"Ошибка при записи списка транзакций: {e}")
            for class_sqlalchemy in list_class_sqlalchemy:
                await AsyncORM.insert_to_db(class_sqlalchemy)

    @staticmethod
    async def insert_to_db(class_sqlalchemy: List[TransactionSQLAlchemy]):
        try:
            async with async_session_factory() as session:
                session.add(class_sqlalchemy)
                await session.commit()
        except Exception as e:
            print(e)
            logger.error(f"Ошибка при записи транзакции: {e}, {class_sqlalchemy}")

    @staticmethod
    async def check_memory_size_table(table_name: str):
        async with async_session_factory() as session:
            result_table = await session.execute(
                text(f"SELECT pg_size_pretty(pg_total_relation_size('{table_name}'));")
            )
            table_size = result_table.scalar()

            return table_size

    @staticmethod
    async def check_memory_size_database():
        async with async_session_factory() as session:
            result_db = await session.execute(text("SELECT pg_size_pretty(pg_database_size(current_database()));"))
            db_size = result_db.scalar()
            return db_size

    @staticmethod
    async def select_transaction() -> List[TransactionDTO]:
        async with async_session_factory() as session:
            query = (
                select(TransactionSQLAlchemy)
            )
            res = await session.execute(query)
            result_orm = res.scalars().all()
            result_dto = [TransactionDTO.model_validate(row, from_attributes=True) for row in result_orm]
            return result_dto

    @staticmethod
    def json_to_dto(transaction_dict) -> TransactionDTO:
        return TransactionDTO(**transaction_dict)

    @staticmethod
    def dto_to_sqlalchemy(dto: TransactionDTO) -> TransactionSQLAlchemy:
        # Преобразуем DTO в модель SQLAlchemy
        return TransactionSQLAlchemy(
            signature=dto.signature,
            mint=dto.mint,
            traderPublicKey=dto.traderPublicKey,
            txType=dto.txType,
            solAmount=dto.solAmount,
            tokenAmount=dto.tokenAmount,
            initialBuy=dto.initialBuy,
            bondingCurveKey=dto.bondingCurveKey,
            newTokenBalance=dto.newTokenBalance,
            vTokensInBondingCurve=dto.vTokensInBondingCurve,
            vSolInBondingCurve=dto.vSolInBondingCurve,
            marketCapSol=dto.marketCapSol,
            name=dto.name,
            symbol=dto.symbol,
            uri=dto.uri,
            pool=dto.pool,
            created_at=datetime.now()
        )