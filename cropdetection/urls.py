from django.conf.urls import url, include

from . import views

app_name = 'cropdetection'

urlpatterns = [
    url(r'^$', view=views.home, name='home'),

    url(r'^marvdasht/$',
        view=views.marvdasht,
        name='marvdasht'),

    url(r'^api/',
        include('cropdetection.api.urls'),
        name='cropdetection_api'),

    url(r'^analyzelist/$',
        view=views.AnalyzeListView.as_view(),
        name='analyze_list'),

    url(r'^analyze/(?P<pk>[0-9A-Fa-f-]+)/$',
        view=views.AnalyzeDetailView.as_view(),
        name='analyze_detail'),

    url(r'^region/(?P<pk>\d+)/$',
        view=views.RegionDetailView.as_view(),
        name='region_detail'),

    url(r'^regions/$',
        view=views.RegionListView.as_view(),
        name='region_list'),

    url(r'^runmarv/(?P<pk>[0-9a-f-]+)/$', view=views.runmarvdasht,
        name="run_marvdasht")
]
