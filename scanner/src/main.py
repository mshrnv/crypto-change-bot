"""Module to search spread"""
import time

import redis

from scanner.src.config import REDIS_HOST, REDIS_PORT, REDIS_DB
from scanner.src.consts import chains
from scanner.src.crypto import get_redis_data, prepare_currencies_data, calc_all_chains_spread
from scanner.src.utils import get_timestamp

PERIOD_TIME = 5  # seconds

if __name__ == '__main__':
    # Redis Connection
    client_db0 = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        charset="utf-8",
        decode_responses=True
    )

    client_db1 = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=1,
        charset="utf-8",
        decode_responses=True
    )

    # Every PERIOD_TIME searching for profitability chains
    while True:
        currencies = get_redis_data(client_db0)
        data = prepare_currencies_data(currencies)
        chain_orders = calc_all_chains_spread(data, chains, client_db1, currencies)

        timestamp = get_timestamp()
        print(f"Цепочки просканированы - {timestamp}")

        time.sleep(PERIOD_TIME)
