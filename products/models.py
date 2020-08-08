from django.db import models

# Create your models here.
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
    url_tag = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.name


class Usage(models.Model):
    name = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.name
