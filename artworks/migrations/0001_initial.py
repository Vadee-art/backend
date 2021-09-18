# Generated by Django 3.1.7 on 2021-09-18 02:55

import artworks.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(
                    max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(
                    blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                 help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255,
                 unique=True, verbose_name='email_address')),
                ('user_name', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('nick_name', models.CharField(blank=True, max_length=150)),
                ('about', models.TextField(blank=True,
                 max_length=500, verbose_name='about')),
                ('created_at', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('profile_picture', models.ImageField(blank=True, upload_to='')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                 related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                 related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('_id', models.AutoField(editable=False,
                 primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True,
                 default='no title', max_length=200, null=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('_id', models.AutoField(editable=False,
                 primary_key=True, serialize=False)),
                ('photo', models.ImageField(
                    default='/defaultImage.png', null=True, upload_to='')),
                ('birthday', models.DateField(default=datetime.date.today)),
                ('biography', models.TextField(blank=True)),
                ('cv', models.TextField(blank=True)),
                ('achievements', models.ManyToManyField(
                    blank=True, to='artworks.Achievement')),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('_id', models.AutoField(editable=False,
                 primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True,
                 default='no title', max_length=200, null=True)),
                ('subtitle', models.CharField(blank=True, max_length=200, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255)),
                ('year', models.CharField(choices=[('1984', '1984'), ('1985', '1985'), ('1986', '1986'), ('1987', '1987'), ('1988', '1988'), ('1989', '1989'), ('1990', '1990'), ('1991', '1991'), ('1992', '1992'), ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), (
                    '2004', '2004'), ('2005', '2005'), ('2006', '2006'), ('2007', '2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021')], default=artworks.models.Artwork.current_year, max_length=200, verbose_name='year')),
                ('print', models.CharField(blank=True, max_length=200, null=True)),
                ('condition', models.CharField(
                    blank=True, max_length=200, null=True)),
                ('edition', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(
                    default='/defaultImage.png', null=True, upload_to='')),
                ('width', models.IntegerField(null=True)),
                ('height', models.IntegerField(null=True)),
                ('depth', models.IntegerField(null=True)),
                ('unit', models.CharField(choices=[
                 ('0', 'in'), ('1', 'cm')], default='', max_length=2)),
                ('is_signed', models.BooleanField(default=False)),
                ('is_authenticated', models.BooleanField(default=False)),
                ('frame', models.CharField(blank=True, max_length=200, null=True)),
                ('isPrice', models.BooleanField(default=False)),
                ('about_work', models.TextField(blank=True)),
                ('art_location', models.TextField(blank=True)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=255)),
                ('in_stock', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('artist', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='artworks.artist')),
            ],
            options={
                'verbose_name_plural': 'Artworks',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('_id', models.AutoField(editable=False,
                 primary_key=True, serialize=False)),
                ('paymentMethod', models.CharField(
                    blank=True, max_length=200, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('shippingPrice', models.DecimalField(
                    blank=True, decimal_places=0, max_digits=7, null=True)),
                ('taxPrice', models.DecimalField(blank=True,
                 decimal_places=0, max_digits=10, null=True)),
                ('totalPrice', models.DecimalField(blank=True,
                 decimal_places=0, max_digits=16, null=True)),
                ('isDelivered', models.BooleanField(default=False)),
                ('deliveredAt', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='artworks.category')),
            ],
            options={
                'verbose_name': 'subCategory',
                'verbose_name_plural': 'subCategories',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('_id', models.AutoField(editable=False,
                 primary_key=True, serialize=False)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('postalcode', models.CharField(
                    blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('deliverymethod', models.CharField(
                    blank=True, max_length=200, null=True)),
                ('order', models.OneToOneField(blank=True, null=True,
                 on_delete=django.db.models.deletion.CASCADE, to='artworks.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('_id', models.AutoField(editable=False,
                 primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(blank=True,
                 decimal_places=0, max_digits=16, null=True)),
                ('image', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('artwork', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='artworks.artwork')),
                ('order', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='artworks.order')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='')),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='artwork_album', to='artworks.artwork')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='image_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('_id', models.AutoField(editable=False,
                 primary_key=True, serialize=False)),
                ('artwork', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='artworks.artwork')),
                ('user', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='artwork',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='product_category', to='artworks.category'),
        ),
        migrations.AddField(
            model_name='artwork',
            name='created_by',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artwork',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='product_sub_category', to='artworks.subcategory'),
        ),
        migrations.AddField(
            model_name='artwork',
            name='tags',
            field=models.ManyToManyField(blank=True, to='artworks.Tag'),
        ),
    ]
