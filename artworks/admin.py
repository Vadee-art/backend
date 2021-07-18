from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Artwork)
admin.site.register(Artist)
admin.site.register(Favorite)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
