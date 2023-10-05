from django.conf import settings
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware

w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER))
account = w3.eth.account.from_key(settings.PRIVATE_KEY)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
