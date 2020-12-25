from rest_framework import serializers


class Festserializer(serializers.Serializer):
    bookid=serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=50)
    price = serializers.FloatField()
 