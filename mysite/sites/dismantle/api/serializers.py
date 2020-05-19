from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from ..models import Predismantle, Postdismantle

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage

IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2  # 2MB
MIN_TITLE_LENGTH = 1
MIN_BODY_LENGTH = 1

from ..utils import is_image_aspect_ratio_valid, is_image_size_valid


# pre instalation
class PredismantleSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = Predismantle
        fields = ['pk', 'title', 'slug', 'description', 'image', 'date_updated', 'username']

    def get_username_from_author(self, pre_dismantle):
        username = pre_dismantle.author.username
        return username

    def validate_image_url(self, pre_dismantle):
        image = pre_dismantle.image
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url

class PredismantleSerializerThumnail(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = Predismantle
        fields = ['pk', 'title', 'slug', 'description', 'image', 'date_updated', 'username']

    def get_username_from_author(self, pre_dismantle):
        username = pre_dismantle.author.username
        return username

    def validate_image_url(self, pre_dismantle):

            #image = survey.image   #// this for full size image
        image = get_thumbnail(pre_dismantle.image,'350x150', crop='center', quality=99)   #this for thumpnile image

        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url

class PredismantleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predismantle
        fields = ['title', 'description', 'image']

    def validate(self, pre_dismantle):
        try:
            title = pre_dismantle['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            body = pre_dismantle['body']
            if len(body) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})

            image = pre_dismantle['image']
            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(location=url)

            with storage.open('', 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            # # Check image size
            # if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
            #     os.remove(url)
            #     raise serializers.ValidationError(
            #         {"response": "That image is too large. Images must be less than 2 MB. Try a different image."})
            #
            # # Check image aspect ratio
            # if not is_image_aspect_ratio_valid(url):
            #     os.remove(url)
            #     raise serializers.ValidationError(
            #         {"response": "Image height must not exceed image width. Try a different image."})

            os.remove(url)
        except KeyError:
            pass
        return pre_dismantle


class PredismantleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predismantle
        fields = ['title', 'description', 'image', 'date_updated', 'author']

    def save(self):

        try:
            image = self.validated_data['image']
            title = self.validated_data['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            description = self.validated_data['description']
            if len(description) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a description longer than " + str(MIN_BODY_LENGTH) + " characters."})

            pre_dismantle = Predismantle(
                author=self.validated_data['author'],
                title=title,
                description=description,
                image=image,
            )

            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(location=url)

            with storage.open('', 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

        #     # Check image size
        #     if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
        #         os.remove(url)
        #         raise serializers.ValidationError(
        #             {"response": "That image is too large. Images must be less than 2 MB. Try a different image."})
        #
        #     # Check image aspect ratio
        #     if not is_image_aspect_ratio_valid(url):
        #         os.remove(url)
        #         raise serializers.ValidationError(
        #             {"response": "Image height must not exceed image width. Try a different image."})
        #
            os.remove(url)
            pre_dismantle.save()
            return pre_dismantle
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a title, some content, and an image."})


# post instalation


class PostdismantleSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = Postdismantle
        fields = ['pk', 'title', 'slug', 'description', 'image', 'date_updated', 'username']

    def get_username_from_author(self, post_dismantle):
        username = post_dismantle.author.username
        return username

    def validate_image_url(self, post_dismantle):
        image = post_dismantle.image
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url


class PostdismantleSerializerThumnail(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = Postdismantle
        fields = ['pk', 'title', 'slug', 'description', 'image', 'date_updated', 'username']

    def get_username_from_author(self, post_dismantle):
        username = post_dismantle.author.username
        return username

    def validate_image_url(self, post_dismantle):

            #image = survey.image   #// this for full size image
        image = get_thumbnail(post_dismantle.image,'350x150', crop='center', quality=99)   #this for thumpnile image

        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url

class PostdismantleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postdismantle
        fields = ['title', 'description', 'image']

    def validate(self, post_dismantle):
        try:
            title = post_dismantle['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            body = post_dismantle['body']
            if len(body) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})

            image = post_dismantle['image']
            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(location=url)

            with storage.open('', 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            # # Check image size
            # if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
            #     os.remove(url)
            #     raise serializers.ValidationError(
            #         {"response": "That image is too large. Images must be less than 2 MB. Try a different image."})
            #
            # # Check image aspect ratio
            # if not is_image_aspect_ratio_valid(url):
            #     os.remove(url)
            #     raise serializers.ValidationError(
            #         {"response": "Image height must not exceed image width. Try a different image."})

            os.remove(url)
        except KeyError:
            pass
        return post_dismantle


class PostdismantleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postdismantle
        fields = ['title', 'description', 'image', 'date_updated', 'author']

    def save(self):

        try:
            image = self.validated_data['image']
            title = self.validated_data['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            description = self.validated_data['description']
            if len(description) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a description longer than " + str(MIN_BODY_LENGTH) + " characters."})

            post_dismantle = Postdismantle(
                author=self.validated_data['author'],
                title=title,
                description=description,
                image=image,
            )

            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(location=url)

            with storage.open('', 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            # # Check image size
            # if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
            #     os.remove(url)
            #     raise serializers.ValidationError(
            #         {"response": "That image is too large. Images must be less than 2 MB. Try a different image."})
            #
            # # Check image aspect ratio
            # if not is_image_aspect_ratio_valid(url):
            #     os.remove(url)
            #     raise serializers.ValidationError(
            #         {"response": "Image height must not exceed image width. Try a different image."})

            os.remove(url)
            post_dismantle.save()
            return post_dismantle
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a title, some content, and an image."})
