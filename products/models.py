from tabnanny import verbose
from django.db import models
from vendors.models import Vendor
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=55)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=55)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
        verbose_name = _('product')
        verbose_name_plural = _('products')


class Image(models.Model):
    pass


