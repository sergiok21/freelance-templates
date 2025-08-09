from rest_framework import serializers


class StatusSerializer(serializers.Serializer):
    all = serializers.BooleanField(required=False)
    user_status = serializers.JSONField(required=False)

    class Meta:
        fields = ['all', 'user_status']

    def validate(self, attrs):
        errors = {}

        if 'all' not in attrs and 'user_status' not in attrs:
            errors['non_field_errors'] = ["One of 'all' or 'user_status' must be provided."]

        if 'all' in attrs and not isinstance(attrs['all'], bool):
            errors['all'] = ["'all' must be a boolean."]

        if 'user_status' in attrs and not isinstance(attrs['user_status'], dict):
            errors['user_status'] = ["'user_status' must be a JSON object."]

        if 'all' in attrs and 'user_status' in attrs:
            errors['non_field_errors'] = ["'all' and 'user_status' cannot both be provided at the same time."]

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class ParserSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    link = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        fields = ['user_id', 'link', 'name']
