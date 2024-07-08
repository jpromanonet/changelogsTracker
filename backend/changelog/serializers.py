from rest_framework import serializers
from .models import Changelog

class ChangelogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Changelog
        fields = '__all__'
