from rest_framework import serializers
from cropdetection import models


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = ['id', 'name', 'last_modified_date']


class AnalyzeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Analyze
        fields = ['id', 'region_name', 'date', 'result', 'color_map']
