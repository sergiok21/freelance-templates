import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError

from category.domain.entities.category_entity import CategoryEntity
from category.interface_adapters.gateways.models import Category
from category.interface_adapters.presenters.api.serializers import CategoryOutSerializer
from category.tests.fakes import FakeCategoryOutEntity, FakeCategoryInEntity


def test_category_serialize():
    fake_entity = FakeCategoryOutEntity()
    entity = CategoryEntity(**fake_entity.__dict__)

    serializer = CategoryOutSerializer(entity)

    assert serializer.data['image'] == '...'


def test_category_deserialize():
    data = FakeCategoryInEntity().__dict__.copy()
    serializer = CategoryOutSerializer(data=data)

    assert serializer.is_valid(raise_exception=True)

    output = FakeCategoryOutEntity().__dict__.copy()

    assert serializer.validated_data['name'] == output['name']
    assert serializer.validated_data['image'] == output['image']


def test_category_field_exists():
    fake_entity = FakeCategoryOutEntity()
    data = fake_entity.__dict__.copy()
    del data['image']

    serializer = CategoryOutSerializer(data=data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_category_serializer():
    category = Category.objects.create(
        name='Індивідуальна',
        price=2000,
        image=SimpleUploadedFile("...", b"img-content", content_type="image/jpeg"),
        description='80 в кольоровій корекції',
        slug='individual'
    )
    serializer = CategoryOutSerializer(category)

    assert serializer.data['image'].startswith('/media/')
