from django.core.management.base import BaseCommand

from artworks.models import Artwork


class Command(BaseCommand):
    help = "Deploy artists contracts"

    def handle(self, *args, **options):
        for artwork in Artwork.objects.all():
            try:
                artwork.upload_image_to_ipfs()
                print(f'Uploaded image of {artwork.pk}')
                artwork.upload_metadata_to_ipfs()
                print(f'Uploaded metadata of {artwork.pk}')
            except Exception as ex:
                print(ex)
