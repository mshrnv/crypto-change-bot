"""Crypto utils"""
from tronpy import Tron


def create_wallet():
    """Creates new TRON wallet"""
    wallet = client.generate_address()
    return wallet


def check_address(address: str) -> bool:
    """Checks if address valid TRON address"""
    return client.is_address(address)


def compress_address(address: str, gap: int = 4) -> str:
    """Compress address like Tg8A...t0E"""
    return address[:gap] + "..." + address[-gap:]


client = Tron()
