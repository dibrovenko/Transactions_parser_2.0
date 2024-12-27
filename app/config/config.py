from dotenv import load_dotenv
import os

load_dotenv()


trade_config = {
    "public_key": os.getenv("PUBLIC_KEY"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "priority_fee": 0.001,
    "slippage": 10,
    "sell_multiplier": 1.1,
    "sell_multiplier_with_social_activity": 1.2,
    "amount": 100
}


token_config = {
    "time_window": 50,  # Время в секундах окна после открытия токена
    "min_buyers": 1,  # Минимальное количество уникальных покупателей, которые должны быть в time_window
    "min_transactions": 5  # Минимальное количество сделок для анализа, которые должны быть в time_window
}


handle_messages_config = {
    "max_tokens": 10000,  # Количество токенов, за которыми нужно следить при их открытии
    "timeout_duration": 100  # Через сколько секунд закрывается соединение, если нет обновлений от pumpfun
}


database_config = {
    "host": "db_auth",  # localhost еще бывает
    "port": 5432,
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "db_name": os.getenv("POSTGRES_DB"),
    "type_connect": "asyncpg",
    "type_db": "postgresql"
}


config = {
    "token_config": token_config,
    "trade_config": trade_config,
    "handle_messages_config": handle_messages_config,
    "database_config": database_config
}


