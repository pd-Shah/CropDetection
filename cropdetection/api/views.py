from rest_framework import generics

from cropdetection import models
from . import serializers

from cropdetection.lib import engine


class RegionListApiView(generics.ListAPIView):
    serializer_class = serializers.RegionSerializer

    def get_queryset(self, ):
        return models.Region.objects.all()


class RegionRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.RegionSerializer

    def get_queryset(self, ):
        return models.Region.objects.all()


class AnalyzeListApiView(generics.ListAPIView):
    serializer_class = serializers.AnalyzeSerializer

    def get_queryset(self, ):
        return models.Analyze.objects.all()


class AnalyzeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.AnalyzeSerializer

    def get_queryset(self, ):
        return models.Analyze.objects.all()


class AnalyzeRetrieveAPIRun(generics.RetrieveAPIView):
    serializer_class = serializers.AnalyzeSerializer

    def get_queryset(self, ):
        engine.connect_engine(self.kwargs['pk'])
        return models.Analyze.objects.all()
