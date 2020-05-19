"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # REST-framework
    path('api/survey/', include('sites.survey.api.urls', 'survey_api')),
    path('api/account/', include('account.api.urls', 'account_api')),
    path('api/preinstalation/', include('sites.instalation.api.pre_urls', 'preinstalation_api')),
    path('api/postinstalation/', include('sites.instalation.api.post_urls', 'postinstalation_api')),
    path('api/predismantle/', include('sites.dismantle.api.pre_urls', 'predismantle_api')),
    path('api/postdismantle/', include('sites.dismantle.api.post_urls', 'postdismantle_api')),
    path('api/sitegps/', include('sites.siteGps.api.urls', 'sitegps_api')),
    path('api/projectmanage/',include('porjectmanage.api.urls', 'porjectmanage_api')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
