from django.contrib import admin
from .models import *

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea

from .models import (
    Category,
    MyUser,
    Order,
    OrderItem,
    Artwork,
    ShippingAddress,
    SubCategory,
)
from admin_searchable_dropdown.filters import AutocompleteFilter


class UserAdminConfig(UserAdmin):
    model = MyUser
    search_fields = ('email', 'user_name', 'first_name',
                     'last_name')
    list_filter = ('email', 'user_name', 'first_name', 'last_name',
                   'profile_picture', 'is_active', 'is_staff')
    ordering = ('-created_at',)
    list_display = ('email', 'user_name', 'first_name', 'last_name', 'profile_picture',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'country', 'city', 'province', 'phone_number', 'postal_code', 'address',
         'first_name', 'last_name', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        MyUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', 'profile_picture', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


class ArtworkArtistFilter(AutocompleteFilter):
    title = 'Artist'  # display title
    field_name = 'artist'  # name of the foreign key field


class ArtistAdminConfig(admin.ModelAdmin):
    model = Artist
    ordering = ('-_id',)
    list_display = ['user', '_id']
    # this is required for django's autocomplete functionality / when adding user to artist
    # search bar / allow reference autocomplete from ArtworkAdminConfig
    search_fields = ['_id']
    autocomplete_fields = ['user']


class ArtworkAdminConfig(admin.ModelAdmin):
    model = Artwork
    ordering = ('-created_at',)
    list_display = ['title', 'artist', 'category', 'origin',
                    'sub_category', 'price', 'created_at', '_id']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = [ArtworkArtistFilter]
    autocomplete_fields = ['artist']


class CategoryAdminConfig(admin.ModelAdmin):
    model = Category
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class OrderAdminConfig(admin.ModelAdmin):
    model = Order
    list_display = ['created_at']


class OrderItemAdminConfig(admin.ModelAdmin):
    model = OrderItem
    list_display = ['created_at']


# Register your models here.
admin.site.register(MyUser, UserAdminConfig)
admin.site.register(Artwork, ArtworkAdminConfig)
admin.site.register(Achievement)
admin.site.register(Artist, ArtistAdminConfig)
admin.site.register(Order, OrderAdminConfig)
admin.site.register(OrderItem, OrderItemAdminConfig)
admin.site.register(Category, CategoryAdminConfig)
admin.site.register(SubCategory)
admin.site.register(Tag)
admin.site.register(ShippingAddress)
admin.site.register(Article)
admin.site.register(Origin)
admin.site.register(TheToken)
admin.site.register(Signature)
