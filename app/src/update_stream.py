import asyncio
import json
import logging
from typing import List

from .token_storage import token_storage

from .websocket_client import ws_client
from config import setup_logger


logger = setup_logger(name=__name__, log_file=__name__, level=logging.INFO)


async def subscribe_token_trade(token_address: str):
    """Подписывается на торговые события для конкретного токена."""
    payload = {
        "method": "subscribeTokenTrade",
        "keys": [token_address]
    }
    websocket = await ws_client.connect()
    await websocket.send(json.dumps(payload))
    logger.debug(f"Подписались на торговые события для токена: {token_address}")


async def subscribe_token_list_trades(token_address_list: List[str]):
    """Подписывается на торговые события для конкретного токена."""
    payload = {
        "method": "subscribeTokenTrade",
        "keys": token_address_list
    }
    websocket = await ws_client.connect()
    await websocket.send(json.dumps(payload))
    logger.info(f"Подписались на торговые события для токенов: {token_address_list}")



async def unsubscribe_token_trade(token_address: str):
    """Отписывается на торговые события для конкретного токена."""
    payload = {
        "method": "unsubscribeTokenTrade",
        "keys": [token_address]
    }
    websocket = await ws_client.connect()
    await websocket.send(json.dumps(payload))
    logger.debug(f"Отписались от торговых событий для токена: {token_address}")
    token_storage.remove_token(token_address)


async def subscribe_new_token():
    """Подписываемся на события создания новых токенов"""
    payload = {
        "method": "subscribeNewToken",
    }
    websocket = await ws_client.connect()
    await websocket.send(json.dumps(payload))
    logger.debug("Подписались на события создания новых токенов.")


async def unsubscribe_new_token():
    """Отписываемся от событий создания новых токенов"""
    payload = {
        "method": "unsubscribeNewToken",
    }
    websocket = await ws_client.connect()
    await websocket.send(json.dumps(payload))
    logger.debug("Отписались от событий создания новых токенов.")