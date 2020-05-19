from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# Predismantle
def Preupload_location(instance, filename, **kwargs):
    file_path = 'predismantle/{author_id}/{title}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename)
    return file_path


class Predismantle(models.Model):
    title = models.CharField(max_length=50, null=False, blank=True)
    description = models.TextField(max_length=5000, null=False, blank=True)
    image = models.ImageField(upload_to=Preupload_location, null=False, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=False)

    def __str__(self):
        return self.title


@receiver(post_delete, sender=Predismantle)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_blog_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


pre_save.connect(pre_save_blog_post_receiever, sender=Predismantle)


#post dismantle
#
def Postupload_location(instance, filename, **kwargs):
    file_path = 'postdismantle/{author_id}/{title}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename)
    return file_path


class Postdismantle(models.Model):
    title = models.CharField(max_length=50, null=False, blank=True)
    description = models.TextField(max_length=5000, null=False, blank=True)
    image = models.ImageField(upload_to=Postupload_location, null=False, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=False)

    def __str__(self):
        return self.title


@receiver(post_delete, sender=Postdismantle)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_blog_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


pre_save.connect(pre_save_blog_post_receiever, sender=Postdismantle)
