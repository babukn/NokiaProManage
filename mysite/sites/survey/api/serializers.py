from rest_framework import serializers
from ..models import Survey
from sorl.thumbnail import get_thumbnail

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage

IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2  # 2MB
MIN_TITLE_LENGTH = 1
MIN_BODY_LENGTH = 1

from ..utils import is_image_aspect_ratio_valid, is_image_size_valid


class SurveySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = Survey
        fields = ['pk', 'title', 'slug', 'description', 'image', 'date_updated', 'username']

    def get_username_from_author(self, survey):
        username = survey.author.username
        return username

    def validate_image_url(self, survey):
        image = survey.image   #// this for full size image
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url

class SurveySerializerThumnail(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = Survey
        fields = ['pk', 'title', 'slug', 'description', 'image', 'date_updated', 'username']

    def get_username_from_author(self, survey):
        username = survey.author.username
        return username

    def validate_image_url(self, survey):

            #image = survey.image   #// this for full size image
        image = get_thumbnail(survey.image,'350x150', crop='center', quality=99)   #this for thumpnile image

        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url

class SurveyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'image']

    def validate(self, survey):
        try:
            title = survey['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            body = survey['body']
            if len(body) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})

            image = survey['image']
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
        return survey


class SurveyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
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

            survey = Survey(
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

            # Check image size
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
            survey.save()
            return survey
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a title, some content, and an image."})
