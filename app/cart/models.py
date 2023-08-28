from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel


class Cart(TimeStampedModel, SoftDeletableModel):
    user = models.ForeignKey('artworks.MyUser', null=False, on_delete=models.DO_NOTHING)
    artworks = models.ManyToManyField('artworks.Artwork', through='CartItem')


class CartItem(TimeStampedModel, SoftDeletableModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    artwork = models.ForeignKey('artworks.Artwork', on_delete=models.CASCADE)
