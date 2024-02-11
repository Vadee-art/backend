from django.conf import settings
from pinatapy import PinataPy

pinata = PinataPy(settings.PINATA_API_KEY, settings.PINATA_SECRET_KEY)


def pin_file_to_ipfs(filepath):
    pin = pinata.pin_file_to_ipfs(filepath, save_absolute_paths=False)
    return pin['IpfsHash']
