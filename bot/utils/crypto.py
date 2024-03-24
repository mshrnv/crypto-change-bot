from tronpy import Tron


def create_wallet():
    wallet = client.generate_address()
    return wallet


def check_address(address):
    return client.is_address(address)


client = Tron()
