from django.urls import path
from ..api.views import api_detail_sitegps_view,api_create_site_gps
app_name = 'sites.siteGps'

urlpatterns = [
    path('', api_detail_sitegps_view.as_view(), name="list"),
    path('create', api_create_site_gps, name="create"),
]
