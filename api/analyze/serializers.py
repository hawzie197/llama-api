from rest_framework import serializers


class UrlQueryParamSerizlizer(serializers.Serializer):
    url = serializers.URLField(required=True, allow_null=False)


class ActionSerializer(serializers.Serializer):
    type = serializers.CharField(read_only=True)
    quote = serializers.CharField(read_only=True)
    confidence = serializers.FloatField(read_only=True)
    classification = serializers.CharField(read_only=True)


class AnalysisSerializer(serializers.Serializer):
    actions = ActionSerializer(many=True, required=True)
    privacy_policy_link = serializers.URLField(required=True)
