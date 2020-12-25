from rest_framework import serializers


class Bookserializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    author = serializers.CharField(max_length=50)
    cover = serializers.CharField(max_length=50)
    topic = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=200)
