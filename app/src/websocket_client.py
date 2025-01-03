import websockets
import ssl
import asyncio
import logging


from config import setup_logger
from db.core import AsyncORM

logger = setup_logger(name=__name__, log_file=__name__, level=logging.INFO)


class WebSocketClient:
    """
    WebSocketClient (Singleton): Класс WebSocketClient реализует паттерн Singleton, то есть при создании нового экземпляра класса возвращается тот же самый объект.
    Это гарантирует, что WebSocket соединение будет установлено только один раз, независимо от того, сколько раз вы обращаетесь к этому классу.
    """

    _instance = None
    _websocket = None

    def __new__(cls, uri: str, ssl_context: ssl.SSLContext):
        if not cls._instance:
            cls._instance = super(WebSocketClient, cls).__new__(cls)
            cls._uri = uri
            cls._ssl_context = ssl_context
        return cls._instance

    async def connect(self):
        """Подключение к WebSocket серверу. Подключение выполняется только один раз."""
        if self._websocket is None:
            self._websocket = await websockets.connect(self._uri, ssl=self._ssl_context)
        return self._websocket

    async def reconnect(self):
        if self._websocket.close:
            from src.update_stream import subscribe_new_token, subscribe_token_list_trades
            retry_max = 5
            retry_count = 0
            if retry_count < retry_max:
                try:
                    logger.info("Пытаемся подключиться к WebSocket серверу.")
                    self._websocket = await websockets.connect(self._uri, ssl=self._ssl_context)
                    unique_mints_last_10_minutes = await AsyncORM.get_unique_mints_last_10_minutes()
                    await subscribe_token_list_trades(token_address_list=unique_mints_last_10_minutes)
                    await subscribe_new_token()
                    logger.info("Успешно переподключились к WebSocket серверу.")
                    return self._websocket
                except Exception as e:
                    retry_count += 1
                    logger.error(f"Ошибка подключения: {e}. Повтор через 0.1 секунду.")
                    await asyncio.sleep(0.1)
        return self._websocket


    async def close(self):
        """Закрытие WebSocket соединения."""
        if self._websocket:
            await self._websocket.close()
            self._websocket = None


# Создаем SSL контекст
# Создаем контекст SSL с отключенной проверкой сертификатов
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# URI для подключения
uri = "wss://pumpportal.fun/api/data"

# Экземпляр WebSocket клиента
ws_client = WebSocketClient(uri, ssl_context)
