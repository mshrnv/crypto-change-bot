import aiohttp
from tronpy import AsyncTron
from tronpy.keys import PrivateKey


# TODO: To delete?
async def transfer_trx(_from, _to, _amount, _private_key):
    async with AsyncTron(network='nile') as client:
        txb = (
            client.trx.transfer(_from, _to, 1_000)
            .fee_limit(100_000_000)
        )

        transaction = await txb.build()
        private_key = PrivateKey(bytes.fromhex(_private_key))

        txn_ret = await transaction.sign(private_key).broadcast()

        return txn_ret


async def transfer_usdt(_from, _to, _amount, _private_key):
    # TODO: TESTNET
    async with (AsyncTron(network='nile') as client):
        private_key = PrivateKey(bytes.fromhex(_private_key))
        # TODO: TESTNET
        usdt_contract_address = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"
        amount_in_wei = int(_amount * 10 ** 6)

        contract = await client.get_contract(usdt_contract_address)

        transfer_data = await contract.functions.transfer(_to, amount_in_wei)
        transfer_data = await transfer_data.with_owner(_from).build()
        transfer_data = transfer_data.sign(private_key)

        tx = await client.broadcast(transfer_data)

        return tx


async def get_wallet_balance(address):
    usdt_contract_address = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        url = f"https://nile.trongrid.io/v1/accounts/{address}"
        async with session.get(url) as resp:
            data = await resp.json()
            trc20 = data.get('data')[0].get('trc20')

            for token in trc20:
                for contract, balance in token.items():
                    if contract == usdt_contract_address:
                        return float(balance) / (10 ** 6)

        return 0
