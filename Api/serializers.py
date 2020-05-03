from rest_framework import serializers
from .models import Link
from django.conf import settings
import os


class linkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = '__all__'

    def create(self, data):
        return Link.objects.create(**data)

    def update(self, instance, validated_data):
        if validated_data.get('url_id'):
            os.rename('./Api/QRs/%s.png' % instance.url_id, './Api/QRs/%s.png' % validated_data['url_id'])
        instance.url_id = validated_data.get('url_id', instance.url_id)
        instance.long_url = validated_data.get('long_url', instance.long_url)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        instance.save()
        return instance

    def to_representation(self, obj):
        data = super().to_representation(obj)

        data['qr_img'] = 'http://{}/QRs/{}'.format(settings.HOST_NAME, data['url_id'] + '.png')
        data['short_url'] = settings.HOST_NAME + '/' + data['url_id']
        data['stats'] = '/stats/' + data['url_id']
        del data['password']
        del data['user']

        return data