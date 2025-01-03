import asyncio
import logging
import json
import websockets

from .websocket_client import ws_client
from .queue_manager import TRANSACTION_QUEUE
from .update_stream import subscribe_new_token, subscribe_token_trade, unsubscribe_new_token

from config import handle_messages_config, setup_logger

logger = setup_logger(name=__name__, log_file=__name__, level=logging.INFO)


async def handle_messages(websocket):
    """Обрабатывает входящие сообщения и подписывается на торговлю токенами при создании нового токена."""
    await subscribe_new_token()
    while True:
        try:
            # Ожидаем сообщение с тайм-аутом
            message = await asyncio.wait_for(websocket.recv(), timeout=handle_messages_config["timeout_duration"])
            message_data = json.loads(message)
            logger.debug(f"Получено сообщение: {message_data}")
            if message_data.get("txType") == "create":
                asyncio.create_task(subscribe_token_trade(token_address=message_data["mint"]))

            if message_data.get("txType") in ["sell", "buy", "create"]:
                # Добавляем транзакцию в очередь
                try:
                    await TRANSACTION_QUEUE.put(message_data)
                except asyncio.QueueFull:
                    logger.warning("Очередь транзакций заполнена. Новые сообщения временно отклоняются.")

        except asyncio.TimeoutError:
            # Если тайм-аут истек
            logger.info(
                f"Тайм-аут истек: не было сообщений в течение {handle_messages_config["timeout_duration"]}секунд.")
            await websocket.close()
            break

        except asyncio.CancelledError:
            logger.exception("Ожидание было отменено")
            await websocket.close()
            break

        except (websockets.ConnectionClosed, websockets.ConnectionClosedError):
            logger.error("Соединение с веб-сокетом разорвано. Переподключение...")
            websocket = await ws_client.reconnect()  # Переподключение
            continue

        except Exception as e:
            logger.exception(f"Необработанная ошибка: {e}")
            break
