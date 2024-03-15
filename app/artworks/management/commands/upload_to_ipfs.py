from backend.sentry import report_exception
from django.core.management.base import BaseCommand

from artworks.models import Artwork


class Command(BaseCommand):
    help = "Upload artworks to ipfs"

    def handle(self, *args, **options):
        for artwork in Artwork.objects.all():
            try:
                if not artwork.image_ipfs_hash:
                    artwork.upload_image_to_ipfs()
                    print(f'Uploaded image of {artwork.pk}')
                if not artwork.metadata_ipfs_hash:
                    artwork.upload_metadata_to_ipfs()
                    print(f'Uploaded metadata of {artwork.pk}')
            except Exception as ex:
                report_exception()
                print(ex)
