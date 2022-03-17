from enum import unique
from tabnanny import verbose
from django.db import models
from vendors.models import Vendor
from users.models import User 
from django.utils.translation import gettext_lazy as _
from PIL import Image

def user_directory_path(instance,filename):
    return 'images/{0}/{1}'.format(instance.vendor, filename)

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(unique=True,null=True)

    def __str__(self):
        return self.image.url 

class Review(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)


