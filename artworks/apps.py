from django.apps import AppConfig


class ArtworksConfig(AppConfig):
    name = 'artworks'

    def ready(self):
        import artworks.signals