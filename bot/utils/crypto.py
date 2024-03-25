"""Crypto utils"""
from tronpy import Tron


def create_wallet():
    """Creates new TRON wallet"""
    wallet = client.generate_address()
    return wallet


def check_address(address):
    """Checks if address valid TRON address"""
    return client.is_address(address)


client = Tron()
