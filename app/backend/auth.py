from artworks.models import MyUser
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist


class Web3AuthBackend(ModelBackend):
    def authenticate(self, address=None):
        try:
            user = MyUser.objects.get(wallet_address=address)
        except ObjectDoesNotExist:
            user = MyUser.objects.create(wallet_address=address, user_name=address)

        return user
