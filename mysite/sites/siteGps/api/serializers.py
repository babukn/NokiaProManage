from rest_framework import serializers

from ..models import SiteGps


class SiteGpsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = SiteGps
        fields = ['site_id', 'long_lang', 'date_updated', 'username']

    def get_username_from_author(self, site_gps):
        username = site_gps.author.username
        return username


class SiteGpsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteGps
        fields = ['site_id', 'long_lang', 'date_updated', 'author']

    def save(self):
        try:
            site_id = self.validated_data['site_id']
            long_lang = self.validated_data['long_lang']
            site_gps = SiteGps(
                site_id=site_id,
                long_lang=long_lang,
                author=self.validated_data['author'],
            )
            site_gps.save()
            return site_gps

        except KeyError:
            raise serializers.ValidationError({"response": "You must have a title, some content, and an image."})
