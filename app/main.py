import asyncio
import logging
from config import setup_logger
from db.core import AsyncORM
from src import (
    save_transactions_to_db,
    handle_messages,
    ws_client
)

logger = setup_logger("main", "main.log", logging.DEBUG)


async def main():
    await AsyncORM.create_tables(flag='restart')
    t = await AsyncORM.select_transaction()
    logger.info(f"длина {len(t)}")

    # Получаем WebSocket соединение (создается только один раз)
    websocket = await ws_client.connect()

    handle_messages_task = asyncio.create_task(handle_messages(websocket=websocket))
    db_task = asyncio.create_task(save_transactions_to_db())

    await asyncio.gather(handle_messages_task, db_task)

    # Закрываем WebSocket соединение при завершении работы
    await ws_client.close()


# Запуск главной функции
if __name__ == "__main__":
    asyncio.run(main())
