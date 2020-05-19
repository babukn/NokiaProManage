from django.urls import path
from ..api.views import (
    pre_api_detail_survey_view,
    pre_api_update_survey_view,
    pre_api_delete_survey_view,
    pre_api_create_survey_view,
    pre_api_is_author_of_survey,
    pre_ApidismantleListView,
    pre_api_full_image_with_pk_view
)

app_name = 'sites.dismantle'

urlpatterns = [
    # preInstalation
    path('<slug>/', pre_api_detail_survey_view, name="detail"),
    path('pk/<int:pk>/', pre_api_full_image_with_pk_view, name="detail"),
    path('<slug>/update', pre_api_update_survey_view, name="update"),
    path('<slug>/delete', pre_api_delete_survey_view, name="delete"),
    path('create', pre_api_create_survey_view, name="create"),
    path('list', pre_ApidismantleListView.as_view(), name="list"),
    path('<slug>/is_author', pre_api_is_author_of_survey, name="is_author"),
]
