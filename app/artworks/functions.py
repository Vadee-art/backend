import json

from backend.web3 import account, w3
from django.conf import settings

from artworks.models import Artist


def deploy_artist_contract(artist: Artist):
    # if artist.contract:
    #     return artist.contract

    with open('app/dapp/app/src/contracts/LazyFactory.sol/LazyFactory.json', 'r') as f:
        contract_interface = json.load(f)

    Contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bytecode'],
    )

    tx = Contract.constructor(
        artist.user.last_name,
        artist.user.last_name,
        '0x77305d566841b9ED0614dc5bF23Fe8858c3D4ab6',  # artist.wallet_address,
        artist.vadee_fee,
        settings.VADEE_ADDRESS,
        artist.royalty_fee,  # 10%
    ).build_transaction(
        {
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
        }
    )
    signed = account.signTransaction(tx)

    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    deployed_addr = receipt["contractAddress"]
    artist.contract = deployed_addr
    artist.save()
