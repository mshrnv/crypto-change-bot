import json
from functools import reduce

import redis

from scanner.src.consts import AMOUNT
from scanner.src.utils import get_timestamp


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
        redis_client: redis.Redis,
        prices: dict,
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

        redis_client.hset(chain, mapping={
            'spread': spread,
            'timestamp': get_timestamp(),
            'orders': json.dumps(orders)
        })

    return None
