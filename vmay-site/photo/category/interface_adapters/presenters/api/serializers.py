from rest_framework import serializers

from category.domain.entities.category_entity import CategoryEntity


class CategoryOutSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField(max_length=128)
    price = serializers.IntegerField()
    image = serializers.URLField(source='image.url')
    description = serializers.CharField()
    slug = serializers.CharField(max_length=128)

    class Meta:
        dataclass = CategoryEntity
