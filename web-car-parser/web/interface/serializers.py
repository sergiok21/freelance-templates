from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import User, Filter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 't_id', 'token', 'is_superuser'
        ]


class FilterSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Filter
        fields = [
            'id', 'user_id', 'name', 'link', 'status'
        ]

    def get_user_id(self, obj):
        return obj.user.t_id

    def clean(self, user, link):
        max_count = 15
        if Filter.objects.filter(user=user).count() >= max_count:
            raise ValidationError('Limit to create filters (15 maximum)')
        if Filter.objects.filter(user=user, link=link).count():
            raise ValidationError('This link exists in your profile')
