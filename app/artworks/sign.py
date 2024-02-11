import sha3
from coincurve.keys import PrivateKey
from django.conf import settings
from eip712_structs import Address, EIP712Struct, String, Uint, make_domain
from eth_utils.encoding import big_endian_to_int

keccak_hash = lambda x: sha3.keccak_256(x).digest()

# Configuration of the EIP712 domain
my_domain = make_domain(
    name='VADEE',
    version='1',
    chainId=settings.CHAIN_ID,
    verifyingContract=settings.CONTRACT_ADDRESS,
)


class Voucher(EIP712Struct):
    artist = Address()
    artworkId = Uint()
    tokenUri = String()
    priceDollar = Uint()
    vadeeFee = Uint()
    royaltyFee = Uint()


def sign(
    artist_address: str,
    artwork_id: int,
    price_dollar: int,
    uri: str,
    vadee_fee: int,
    royalty_fee: int,
):
    msg = Voucher()
    msg['artist'] = artist_address
    msg['artworkId'] = artwork_id
    msg['priceDollar'] = price_dollar
    msg['tokenUri'] = uri
    msg['vadeeFee'] = vadee_fee
    msg['royaltyFee'] = royalty_fee

    signable_bytes = msg.signable_bytes(my_domain)
    pk = PrivateKey.from_hex(settings.SIGNER_PRIVATE_KEY[2:])
    signature = pk.sign_recoverable(signable_bytes, hasher=keccak_hash)
    v = signature[64] + 27
    r = big_endian_to_int(signature[0:32])
    s = big_endian_to_int(signature[32:64])

    final_sig = r.to_bytes(32, 'big') + s.to_bytes(32, 'big') + v.to_bytes(1, 'big')

    return '0x' + final_sig.hex()
