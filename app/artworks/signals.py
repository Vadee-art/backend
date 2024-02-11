from cart.models import Cart
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from artworks.models import Artwork, MyUser


# when email is changed user name is changed
def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email != '':
        user.username = user.email


pre_save.connect(updateUser, sender=User)


@receiver(post_save, sender=MyUser)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=Artwork)
def artwork_post_save(sender, instance, created, **kwargs):
    if created or instance.signature:
        instance.sign()

    if not instance.image_ipfs_hash:
        instance.upload_image_to_ipfs()

    if not instance.metadata_ipfs_hash:
        instance.upload_metadata_to_ipfs()
