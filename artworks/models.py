from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as __
from django.conf import settings
from django.urls import reverse
from datetime import date
from django.utils import timezone


from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    User,
)


class MyUserManager(BaseUserManager):
    # super user
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name,  password, **other_fields)

    # normal user
    def create_user(self, email, user_name, first_name,  password, **other_fields):
        if not email:
            # _ if translation needed later
            raise ValueError(__('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email_address', max_length=255, unique=True, blank=False)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=150, blank=True)
    postal_code = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=250, blank=True)
    about = models.TextField(__('about'), max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(upload_to='', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'user_name']
    # Email & Password are required by default

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def __str__(self):
        return self.email


class Achievement(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=200, null=True,
                             blank=True, default='no title')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


# Using settings.AUTH_USER_MODEL will delay the retrieval of the actual model class until all apps are loaded.
class Artist(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    photo = models.ImageField(null=True, default='/defaultImage.png')
    birthday = models.DateField(default=date.today)
    nationality = models.CharField(max_length=255, db_index=True)
    biography = models.TextField(blank=True)
    cv = models.TextField(blank=True)
    achievements = models.ManyToManyField(Achievement, blank=True)
    favorites = models.ManyToManyField(
        MyUser, related_name='favorite_artist', default=None, blank=True)

    class Meta:
        verbose_name = 'artist'

    def __str__(self):
        return self.user.first_name


class Tag(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(null=True, default='/defaultImage.png')

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'sub category'
        verbose_name_plural = 'sub categories'

    def __str__(self):
        return self.name


class Origin(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    country = models.CharField(max_length=255, db_index=True, default='')
    city = models.CharField(max_length=255, db_index=True, default='')

    def __str__(self):
        return self.country


class ArtworkManager(models.Manager):
    def get_queryset(self):
        return super(ArtworkManager, self).get_queryset().filter(is_active=True)


class Artwork(models.Model):
    UNITS = (
        ('0', 'in'),
        ('1', 'cm'),
    )

    def year_choices():
        return [(str(r), str(r)) for r in range(1984, date.today().year+1)]

    def current_year():
        return str((date.today().year))

    _id = models.AutoField(primary_key=True, editable=False)
    artist = models.ForeignKey(
        Artist, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, related_name='product_category', on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        SubCategory, related_name='product_sub_category', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True,
                             blank=True, default='no title')
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=255, blank=True)

    year = models.CharField(
        _('year'), choices=year_choices(), default=current_year, max_length=200)

    print = models.CharField(max_length=200, null=True, blank=True)
    condition = models.CharField(max_length=200, null=True, blank=True)
    edition = models.CharField(max_length=200, null=True, blank=True)
    # uploads to MEDIA_ROOT in setting
    image = models.ImageField(null=True, default='/defaultImage.png')
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    depth = models.IntegerField(null=True)
    unit = models.CharField(max_length=2, choices=UNITS, default="")
    is_signed = models.BooleanField(null=False, default=False)
    is_authenticated = models.BooleanField(null=False, default=False)
    frame = models.CharField(max_length=200, null=True, blank=True)
    isPrice = models.BooleanField(null=False, default=False)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    about_work = models.TextField(blank=True)
    origin = models.ForeignKey(Origin, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=False, default=1)
    tags = models.ManyToManyField(Tag, blank=True)
    price = models.IntegerField(null=False)
    favorites = models.ManyToManyField(
        MyUser, related_name='favorite_artworks', default=None, blank=True)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_carousel = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        MyUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ArtworkManager()

    class Meta:
        verbose_name = 'artwork'
        verbose_name_plural = 'artworks'
        ordering = ('-created_at',)

    # e.g in django template,get URL links for all products by calling this
    def get_absolute_url(self):
        return reverse('artworks: artwork_detail', args=[self.slug])

    def __str__(self):
        return self.title


class Order(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=0, null=True, blank=True)
    taxPrice = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=16, decimal_places=0, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)

# cart


class OrderItem(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    artwork = models.ForeignKey(Artwork, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=False)
    price = models.DecimalField(
        max_digits=16, decimal_places=0, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    postalcode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'shipping addresses'

    def __str__(self):
        return self.address


class Article(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title
