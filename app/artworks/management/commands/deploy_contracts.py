from django.core.management.base import BaseCommand

from artworks.functions import deploy_artist_contract
from artworks.models import Artist


class Command(BaseCommand):
    help = "Deploy artists contracts"

    def handle(self, *args, **options):
        for artist in Artist.objects.all():
            deploy_artist_contract(artist)
