from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

from . import views

swagger = get_swagger_view(title='Public API')

urlpatterns = [
    url(r'^region/$',
        view=views.RegionListApiView.as_view(),
        name='region_list_api'),

    url(r'^region/(?P<pk>\d+)/$',
        view=views.RegionRetrieveAPIView.as_view(),
        name='region_detail_api'),

    url(r'^analyze/$',
        view=views.AnalyzeListApiView.as_view(),
        name='analyze_list_api'),

    url(r'^analyze/(?P<pk>[0-9A-Fa-f-]+)/$',
        view=views.AnalyzeRetrieveAPIView.as_view(),
        name='analyze_detail_api'),

    url(r'^analyze/(?P<pk>[0-9A-Fa-f-]+)/run/$',
        view=views.AnalyzeRetrieveAPIRun.as_view(),
        name='analyze_detail_api_run'),

    url(r'^swagger/$', view=swagger, name='swagger'),

]
