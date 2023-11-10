from datetime import date
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as __
from django_cte import CTEManager
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from rest_framework.exceptions import ValidationError as HTTPValidationError


class TheMarketPlace(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    contract = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_variable = models.FloatField(default=1, unique=True)
    low_boundary = models.IntegerField(default=150, unique=True)  # 100 dollar
    mid_boundary = models.IntegerField(default=1000, unique=True)  # 500 dollar
    low_boundary_constant = models.FloatField(default=10, unique=True)  # 10 dollar
    mid_boundary_percentage = models.FloatField(default=0.02, unique=True)  # 2%
    high_boundary_percantage = models.FloatField(default=0.05, unique=True)  # 5%

    class Meta:
        verbose_name = "Market Place"

    def fetch_transaction_fee(self, price):  # price in dollar
        if price < self.low_boundary:
            transaction_fee = self.low_boundary_constant
            shipping_price = self.shipping_variable * 50

        elif self.low_boundary < price < self.mid_boundary:
            transaction_fee = self.mid_boundary_percentage * price
            shipping_price = self.shipping_variable * 100
        else:
            transaction_fee = self.high_boundary_percantage * price
            shipping_price = self.shipping_variable * 150

        return {"transaction_fee": transaction_fee, "shipping_price": shipping_price}

    def __str__(self):
        return str(self.created_at)


class UserManager(BaseUserManager):
    # super user
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, user_name, first_name, password, **other_fields)

    # normal user
    def create_user(self, email, user_name, first_name, password, **other_fields):
        if not email:
            # _ if translation needed later
            raise ValueError(__("You must provide an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email_address", max_length=255, unique=True, null=True, blank=True
    )
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    province = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=150, blank=True)
    postal_code = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=250, blank=True)
    about = models.TextField(__("about"), max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(upload_to="", blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    wallet_address = models.CharField(max_length=250, null=True, blank=True)

    followed_artists = models.ManyToManyField('Artist', related_name='followers')

    city = models.ForeignKey(
        'cities_light.City',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "user_name"]
    # Email & Password are required by default

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email


class Achievement(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=200, null=True, blank=True, default="no title")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        tags_count = Tag.objects.filter(name__contains=self.name).count()
        if tags_count > 0:
            return
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Genre(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(null=True, default="/defaultImage.png")
    show_in_homepage = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "genre"
        verbose_name_plural = "genre"

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


class Technique(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


class Origin(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    country = models.CharField(max_length=255, db_index=True, default="")
    city = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True)
    flag = models.ImageField(null=True, default="/defaultImage.png")
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.country


class Artist(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    wallet_address = models.CharField(max_length=255, blank=True)
    gallery_address = models.CharField(max_length=250, blank=True)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="artist")
    photo = models.ImageField(null=True, default="/defaultImage.png")
    birthday = models.DateField(default=date.today)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE, null=False)
    biography = models.TextField(blank=True)
    cv = models.TextField(blank=True)
    achievements = models.ManyToManyField(Achievement, blank=True)
    favorites = models.ManyToManyField(
        MyUser, related_name="favorite_artist", default=None, blank=True
    )
    contract = models.CharField(max_length=64, blank=True)
    vadee_fee = models.IntegerField(default=10)
    royalty_fee = models.IntegerField(default=10)
    is_featured = models.BooleanField(default=False)
    similar_artists = models.ManyToManyField('Artist', symmetrical=True)

    class Meta:
        verbose_name = "artist"

    def __str__(self):
        return self.user.email


class Voucher(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=350)
    artwork_id = models.ForeignKey('Artwork', on_delete=models.CASCADE, related_name='vouchers')
    edition = models.IntegerField()
    price_wei = models.IntegerField()
    price_dollar = models.IntegerField()
    content = models.CharField(max_length=350, default="")
    signature = models.CharField(max_length=350)
    is_sold = models.BooleanField(default=False)

    class Meta:
        verbose_name = "voucher"

    def __str__(self):
        return self.token_uri

    @property
    def token_uri(self):
        return urljoin(settings.DOMAIN, f'/tokens/{self._id}')

    def delete(self, *args, **kwargs):
        if self.is_sold:
            raise HTTPValidationError('Cannot delete sold vouchers')
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.is_sold:
            raise HTTPValidationError('Cannot update sold vouchers')
        return super().save(*args, **kwargs)


class Collection(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=350, blank=True)

    class Meta:
        verbose_name = "collection"

    def __str__(self):
        return self.title


class ArtworkManager(CTEManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_active=True)
            .select_related(
                'artist',
                'collection',
                'genre',
                'artist__user',
                'owner',
                'artist__origin',
                'theme',
                'technique',
            )
            .prefetch_related('tags', 'artist__achievements', 'artist__favorites')
        )


class SimpleArtworkManager(CTEManager):
    def get_queryset(self):
        return super().get_queryset()


class Artwork(models.Model):
    UNITS = (
        ("0", "cm"),
        ("1", "in"),
    )

    def year_choices():
        return [(str(r), str(r)) for r in range(1884, date.today().year + 1)]

    def current_year():
        return str((date.today().year))

    def validate(value):
        if value == 0:
            raise ValidationError(
                _("%(value)s is not valid for total edition"),
                params={"value": value},
            )

    def clean(self):
        if self.edition_total < self.edition_number:
            raise ValidationError("total edition must be greater than edition number")
        super(Artwork, self).clean()

    _id = models.AutoField(primary_key=True, editable=False)
    genre = models.ForeignKey(
        Genre, related_name="genre_artworks", on_delete=models.CASCADE, null=True
    )
    theme = models.ForeignKey(
        Theme, related_name="them_artworks", on_delete=models.CASCADE, null=True
    )
    technique = models.ForeignKey(
        Technique, related_name="technique_artworks", on_delete=models.CASCADE, null=True
    )
    title = models.CharField(max_length=200, null=True, blank=True, default="no title")
    collection = models.OneToOneField(Collection, on_delete=models.CASCADE, null=True, blank=True)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    year = models.CharField(_("year"), choices=year_choices(), default=current_year, max_length=200)
    print = models.CharField(max_length=200, null=True, blank=True)
    condition = models.CharField(max_length=200, null=True, blank=True)
    # uploads to MEDIA_ROOT in setting
    image = models.ImageField(null=False, blank=False, default="/defaultImage.png")
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    depth = models.IntegerField(null=True, blank=True)
    unit = models.CharField(max_length=2, choices=UNITS, default="")
    frame = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    about_work = models.TextField(blank=True)
    # origin = models.ForeignKey(Origin, on_delete=models.SET_NULL, null=True)
    edition_number = models.IntegerField(null=False, default=1)
    edition_total = models.IntegerField(null=False, default=0, validators=[validate])
    tags = models.ManyToManyField(Tag, blank=True)
    price = models.IntegerField(null=False)
    quantity = models.IntegerField(default=1)

    # price_eth = models.CharField(max_length=200, null=True, blank=True)
    # favorite_artworks = models.ManyToManyField(MyUser, related_name="user_favorite_artworks", default=None, blank=True)
    is_minted = models.BooleanField(default=False)
    on_market = models.BooleanField(default=False)
    is_artist_talented = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_sold_out = models.BooleanField(default=False)
    is_notable = models.BooleanField(default=False)
    is_carousel = models.BooleanField(default=False)
    owner = models.ForeignKey(
        MyUser,
        on_delete=models.SET_NULL,
        related_name="artwork_owner",
        null=True,
        blank=True,
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="artworks",
        null=False,
        blank=False,
    )

    created_by = models.ForeignKey(
        MyUser, on_delete=models.SET_NULL, related_name="artwork_creator", null=True
    )  # add artwork from panel
    created_at = models.DateTimeField(auto_now_add=True)

    image_medium_quality = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=720, upscale=False)],
        format='JPEG',
        options={'quality': 95},
    )

    similar_artworks = models.ManyToManyField('Artwork', symmetrical=True)

    objects = ArtworkManager()
    simple_object = SimpleArtworkManager()

    class Meta:
        verbose_name = "artwork"
        verbose_name_plural = "artworks"
        ordering = ("-created_at",)

    def __str__(self):
        return str(self._id)

    # e.g in django template,get URL links for all artworks by calling this
    def get_absolute_url(self):
        return reverse("artworks: artwork_detail", args=[self.slug])


class TheToken(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.SET_NULL,
        related_name="token_artwork",
        null=True,
        blank=True,
    )
    token_id = models.CharField(max_length=250, null=True, blank=True, unique=True)
    market_item_id = models.CharField(max_length=250, null=True, blank=True)
    holder = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    contract = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = "NFT"

    def __str__(self):
        return str(self.token_id)


class Order(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    seller = models.ForeignKey(
        MyUser, on_delete=models.SET_NULL, related_name="order_seller", null=True
    )
    buyer = models.ForeignKey(
        MyUser, on_delete=models.SET_NULL, related_name="order_buyer", null=True
    )
    transaction_hash = models.CharField(max_length=200, null=True, blank=True)
    price_eth = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    fee_eth = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self._id)


class ShippingAddress(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    buyer = models.ForeignKey(
        MyUser, on_delete=models.SET_NULL, related_name="buyer_shipping", null=True
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    province = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    postal_code = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "shipping addresses"

    def __str__(self):
        return self.address


class Article(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title
