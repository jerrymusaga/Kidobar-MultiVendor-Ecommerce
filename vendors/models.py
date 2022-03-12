from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    creator = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='vendor', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')

    def __str__(self):
        return self.name
