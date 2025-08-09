from rest_framework import serializers

from .models import DataModel


class TelegramAPISerializer(serializers.Serializer):
    name = serializers.CharField()
    link = serializers.URLField()
    price = serializers.CharField(allow_null=True)
    description = serializers.JSONField(allow_null=True)
    location = serializers.JSONField(allow_null=True)
    telephones = serializers.ListField()
    user_link = serializers.URLField()
    user_link_name = serializers.CharField()

    class Meta:
        fields = ['name', 'link', 'description', 'location', 'telephones', 'user_link', 'user_link_name']

    def create(self, validated_data):
        return DataModel(**validated_data)
