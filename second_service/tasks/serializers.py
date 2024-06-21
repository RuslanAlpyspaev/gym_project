from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    environment = serializers.CharField(max_length=100)
