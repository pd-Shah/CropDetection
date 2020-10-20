from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .lib.engine import marvdasht
from . import models
from cropdetection.lib import engine


class AnalyzeListView(generic.ListView):
    template_name = 'cropdetection/analyze_list.html'
    model = models.Analyze
    paginate_by = 10


class AnalyzeDetailView(generic.DetailView):
    template_name = "cropdetection/analyze_detail.html"
    model = models.Analyze
    paginate_by = 10


class RegionListView(generic.ListView):
    template_name = 'cropdetection/region_list.html'
    model = models.Region
    paginate_by = 10


class RegionDetailView(generic.DetailView):
    template_name = 'cropdetection/region_detail.html'
    model = models.Region
    paginate_by = 10


def home(request, ):
    return render(
        request=request,
        template_name='cropdetection/home.html',
        )


def marvdasht(request,  ):
    return render(
        request=request,
        template_name='cropdetection/marvdasht.html',
        )
    
def runmarvdasht(request, pk):
    engine.marvdasht(pk)
    return HttpResponse('ds')
