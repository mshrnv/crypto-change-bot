import json
from tronpy import Tron


def create_wallet():
    wallet = client.generate_address()
    return wallet


def is_valid(address):
    try:
        client.is_address(address)
        return True
    except Exception as e:
        return False


def send_usdt(recipient_address, amount):
    if is_valid(recipient_address):
        private_key = 'YOUR_PRIVATE_KEY'
        client.private_key = private_key
        transaction = client.transaction_builder.send_trx(recipient_address, amount, 'USDT')
        signed_transaction = client.trx.sign(transaction)
        response = client.trx.broadcast(signed_transaction)
        print(response['transaction']['txID'])
    else:
        print("Error NOT valid adress:" + recipient_address)


client = Tron()

print(create_wallet())
