from rest_framework import serializers

from images.models import Images


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        # fields = '__all__'
        fields = ('id', 'Url', 'CreateDate')
