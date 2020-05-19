from django.conf import settings
from django.db import models


class SiteGps(models.Model):
    site_id = models.CharField(max_length=20, null=False, blank=False)
    long_lang = models.CharField(max_length=40, null=False, blank=False)
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)