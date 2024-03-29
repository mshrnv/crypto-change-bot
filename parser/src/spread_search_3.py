"""Module to search spread"""
from functools import reduce
import time
import pymongo
import redis

from src.config import REDIS_HOST, REDIS_PORT, REDIS_DB, MONGO_HOST, MONGO_PORT, MEXC_ACCESS_KEY, MEXC_SECRET_KEY
from src.consts import chains, AMOUNT
from src.mexc import MexcClient
from src.utils import get_timestamp


def get_redis_data(redis_client: redis.Redis):
    """Returns all data from Redis"""
    data = {}
    keys = redis_client.keys('*')
    for key in keys:
        data[key] = redis_client.hgetall(key)

    return data


def prepare_currencies_data(currencies_data: dict):
    """Transform currencies dict data to (c1, c1): [ask|bid]"""
    data = {}
    for ticker, values in currencies_data.items():
        # All currencies have 3-letter name
        if 'MX' in ticker:
            ccy1, ccy2 = ticker[:2], ticker[2:]
        else:
            ccy1, ccy2 = ticker[:3], ticker[3:]

        data[(ccy1, ccy2)] = float(values['bid'])
        data[(ccy2, ccy1)] = 1 / float(values['ask'])

    return data


def calc_chain_spread(crypto_chain: list) -> float:
    """Calculating spred of chain"""
    result = reduce(lambda x, y: x * y, crypto_chain)
    spread = result * 100 - 100
    return spread


def calc_all_chains_spread(
        weights: dict,
        all_chains: list,
        mongo_collection: pymongo.collection,
        prices: dict,
        min_spread: float = 0.7
):
    """Chains bruteforce for profitability and saving to MongoDB"""

    for chain in all_chains:
        chain_path = [
            weights[(chain[0], chain[1])],
            weights[(chain[1], chain[2])],
            weights[(chain[2], chain[3])],
        ]

        if chain[1] in ['BTC', 'ETH']:
            mid_symbol = chain[2] + chain[1]
            mid_side = 'BUY'
        else:
            mid_symbol = chain[1] + chain[2]
            mid_side = 'SELL'

        orders = [
            {
                'symbol': chain[1] + chain[0],
                'side': 'BUY',
                'type': 'LIMIT',
                'price': prices[chain[1] + chain[0]]['ask'],
                'quantity': AMOUNT * weights[(chain[0], chain[1])]
            },
            {
                'symbol': mid_symbol,
                'side': mid_side,
                'type': 'LIMIT',
                'price': prices[mid_symbol]['ask' if mid_side == 'BUY' else 'bid'],
                'quantity': AMOUNT * weights[(chain[0], chain[1])] * weights[(chain[1], chain[2])]
            },
            {
                'symbol': chain[2] + chain[3],
                'side': 'SELL',
                'type': 'LIMIT',
                'price': prices[chain[2] + chain[3]]['bid'],
                'quantity': AMOUNT * weights[(chain[0], chain[1])] * weights[(chain[1], chain[2])]
            }
        ]

        spread = round(calc_chain_spread(chain_path), 4)
        mongo_collection.insert_one({
            "chain": chain,
            "spread": spread,
            "timestamp": get_timestamp()
        })

        print('-----------------')
        print(*chain, sep=' -> ')
        print('Spread: ' + str(spread) + '%')

        if spread >= min_spread:
            print(f'SPREAD >= {min_spread} FOUNDED')
            return orders

    return None


if __name__ == '__main__':
    # Redis Connection
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        charset="utf-8",
        decode_responses=True
    )

    # MongoDB Connection
    mongo_client = pymongo.MongoClient(
        MONGO_HOST,
        MONGO_PORT,
    )

    mexc_client = MexcClient(
        api_key=MEXC_ACCESS_KEY,
        api_secret=MEXC_SECRET_KEY
    )

    # DB: crypto
    db = mongo_client.crypto
    # Collection: mexc_spreads_3
    mongo_spreads = db.mexc_spreads_3

    # Every 10sec searching for profitability chains
    while True:
        currencies = get_redis_data(client)
        data = prepare_currencies_data(currencies)
        chain_orders = calc_all_chains_spread(data, chains, mongo_spreads, currencies)

        if chain_orders is not None:
            break

        time.sleep(3)

    for order in chain_orders:
        res = mexc_client.new_order(order)
        print(res)
        time.sleep(3)  # make constant
