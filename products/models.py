from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Brand(models.Model):
    name = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(blank=False, max_length=50)
    cat_no = models.IntegerField(blank=False)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class Usage(models.Model):
    name = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(blank=False, max_length=50)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    desc = models.TextField(blank=False, max_length=500)
    origin = models.ForeignKey('Country', on_delete=models.CASCADE)
    weight_per_pack = models.FloatField(blank=False)
    qty_per_pack = models.IntegerField(blank=True, null=True)
    barcode_spec = models.CharField(blank=True, max_length=3)
    barcode_no = models.BigIntegerField(blank=True, null=True)
    image = models.URLField(blank=False)
    root_price = models.DecimalField(max_digits=10, decimal_places=3,
                                     blank=False)
    multiplier = models.DecimalField(max_digits=5, decimal_places=3,
                                     blank=False, default=1.00)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    subcategory = models.ManyToManyField(Subcategory)
    usage = models.ManyToManyField('Usage')
    editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_edited = models.DateTimeField(auto_now_add=True, blank=True)

    SALE_STATUS = (
        ('b', 'Best Sellers'),
        ('d', 'Bulk Discount'),
        ('n', 'Normal'),
        ('o', 'On Offer')
    )

    status = models.CharField(
        max_length=1,
        choices=SALE_STATUS,
        blank=True,
        default='n',
        help_text='Product Sale Status',
    )

    def __str__(self):
        return self.name

    def get_current_price(self):
        return self.root_price * self.multiplier
