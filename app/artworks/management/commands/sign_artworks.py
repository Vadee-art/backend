from backend.sentry import report_exception
from django.core.management.base import BaseCommand

from artworks.models import Artwork


class Command(BaseCommand):
    help = "Sign artworks"

    def handle(self, *args, **options):
        for artwork in Artwork.objects.all():
            if artwork.signature:
                continue
            try:
                artwork.sign()
                print(f'Signed {artwork.pk}')
            except Exception as ex:
                report_exception()
                print(ex)
