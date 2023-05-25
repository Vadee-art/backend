from django.contrib import admin
from .models import *

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.utils.safestring import mark_safe

from .models import (
    Category,
    User,
    Collection,
    Order,
    Artwork,
    ShippingAddress,
    SubCategory,
)
from admin_searchable_dropdown.filters import AutocompleteFilter


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ("email", "user_name", "first_name", "last_name")
    list_filter = (
        "email",
        "user_name",
        "first_name",
        "last_name",
        "profile_picture",
        "is_active",
        "is_staff",
    )
    ordering = ("-created_at",)
    list_display = (
        "email",
        "user_name",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "user_name",
                    "country",
                    "city",
                    "province",
                    "phone_number",
                    "postal_code",
                    "address",
                    "first_name",
                    "last_name",
                    "profile_picture",
                    "wallet_address",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Personal", {"fields": ("about",)}),
    )
    formfield_overrides = {
        User.about: {"widget": Textarea(attrs={"rows": 10, "cols": 40})},
    }
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "user_name",
                    "first_name",
                    "last_name",
                    "profile_picture",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


class ArtworkArtistFilter(AutocompleteFilter):
    title = "Artist"  # display title
    field_name = "artist"  # name of the foreign key field


class ArtistAdminConfig(admin.ModelAdmin):
    model = Artist
    ordering = ("-_id",)
    list_display = ["user", "_id", "gallery_address"]
    # this is required for django's autocomplete functionality / when adding user to artist
    # search bar / allow reference autocomplete from ArtworkAdminConfig
    search_fields = ("user",)
    autocomplete_fields = ["user"]


class ArtworkAdminConfig(admin.ModelAdmin):
    model = Artwork
    ordering = ("-created_at",)
    list_display = [
        "_id",
        "title",
        "current_image",
        "collection",
        "is_artist_talented",
        "is_notable",
        "is_carousel",
        "on_market",
        "artist",
        "category",
        "origin",
        "sub_category",
        "price",
        "image",
        "created_at",
    ]
    exclude = ("is_active", "on_market", "is_minted", "is_sold_out")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = [ArtworkArtistFilter]
    autocomplete_fields = ("artist", "tags")
    # readonly_fields = ["current_image"]

    def current_image(self, obj):
        return mark_safe(
            '<img src="/media/{url}" width="50" height=50 border=1/>'.format(
                url=obj.image,
            )
        )


class CategoryAdminConfig(admin.ModelAdmin):
    model = Category
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class OrderAdminConfig(admin.ModelAdmin):
    model = Order
    list_display = ["_id", "created_at", "transaction_hash", "price_eth", "fee_eth"]


class ShippingAddressAdminConfig(admin.ModelAdmin):
    model = ShippingAddress
    list_display = ["_id", "city", "country", "phone", "order"]


class TagAdminConfig(admin.ModelAdmin):
    model = Tag
    search_fields = ["name"]


# Register your models here.
admin.site.register(User, UserAdminConfig)
admin.site.register(Artwork, ArtworkAdminConfig)
admin.site.register(Achievement)
admin.site.register(Artist, ArtistAdminConfig)
admin.site.register(Order, OrderAdminConfig)
admin.site.register(Category, CategoryAdminConfig)
admin.site.register(SubCategory)
admin.site.register(Tag, TagAdminConfig)
admin.site.register(ShippingAddress, ShippingAddressAdminConfig)
admin.site.register(Collection)
admin.site.register(Article)
admin.site.register(Origin)
admin.site.register(TheMarketPlace)
admin.site.register(TheToken)
admin.site.register(Voucher)
