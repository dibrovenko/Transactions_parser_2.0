import asyncio
import time
import logging
from asyncio import Queue


from db.core import AsyncORM
from config import setup_logger
logger = setup_logger(name=__name__, log_file=__name__, level=logging.INFO)


# Потокобезопасная очередь с ограничением размера
QUEUE_MAX_SIZE = 100000  # Максимум транзакций в очереди
BATCH_SIZE = 1000      # Размер батча для записи в базу данных
TRANSACTION_QUEUE = Queue(maxsize=QUEUE_MAX_SIZE)


async def save_transactions_to_db():
    """Сохраняет транзакции в базу данных батчами."""
    logger.info("Запуск фонового процесса cохранение транзакциий в базу данных батчами")
    while True:
        try:
            # Собираем батч транзакций
            transactions_to_save = []
            for _ in range(BATCH_SIZE):
                try:
                    # Ждем, пока очередь предоставит следующую транзакцию
                    transaction_json = await asyncio.wait_for(TRANSACTION_QUEUE.get(), timeout=100)
                    transaction_dto = AsyncORM.json_to_dto((transaction_json))
                    transaction_sqlalchemy = AsyncORM.dto_to_sqlalchemy(transaction_dto)
                    transactions_to_save.append(transaction_sqlalchemy)
                except asyncio.TimeoutError:
                    logger.info(f"Если очередь пуста и прошло время ожидания, записываем последние транзакции в базу данных")
                    break
                except Exception as e:
                    logger.error(f"Ошибка при обработки транзакции: {e}, {transaction_json}")

            if not transactions_to_save:
                logger.info("Нет транзакций для записи в базу данных.")
                break

            # Запись батча в базу данных
            logger.info(f"Начинаем запись {len(transactions_to_save)} транзакций в базу данных.")
            await AsyncORM.insert_list_to_db(list_class_sqlalchemy=transactions_to_save)

            # Уведомляем очередь, что обработка транзакций завершена
            for _ in transactions_to_save:
                TRANSACTION_QUEUE.task_done()

        except asyncio.CancelledError:
            logger.info("Ожидание было отменено")
        except Exception as e:
            logger.error(f"Ошибка при записи транзакций в базу данных: {e}")




