"""Live parsing module of OKX market"""
import time

import redis

from mexc import MexcClient
from parser.src.config import REDIS_HOST, REDIS_PORT, REDIS_DB, MEXC_ACCESS_KEY, MEXC_SECRET_KEY
from parser.src.utils import get_timestamp

PERIOD_TIME = 5
TIMEOUT = 10

if __name__ == "__main__":
    # Connection with Redis
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB
    )

    # MEXC client
    mexc = MexcClient(
        api_key=MEXC_ACCESS_KEY,
        api_secret=MEXC_SECRET_KEY
    )

    # Every 3sec updating redis with new tickers
    while True:
        tickers = mexc.get_data()

        if not tickers:
            time.sleep(TIMEOUT)
            continue

        timestamp = get_timestamp()
        print(f"Получены тикеры - {timestamp}")

        for ticker, data in tickers.items():
            # Structure of Redis item
            client.hset(ticker, mapping={
                'ask': data['ask'],
                'bid': data['bid'],
                'ask_size': data['ask_size'],
                'bid_size': data['bid_size'],
            })

        time.sleep(PERIOD_TIME)
