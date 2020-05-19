from django.urls import path
from ..api.views import (
    post_api_detail_survey_view,
    post_api_update_survey_view,
    post_api_delete_survey_view,
    post_api_create_survey_view,
    post_api_is_author_of_survey,
    post_ApiSurveyListView,
    post_api_full_image_with_pk_view,
)

app_name = 'sites.instalation'

urlpatterns = [  # post Instalation
    path('<slug>/', post_api_detail_survey_view, name="detail"),
    path('pk/<int:pk>/', post_api_full_image_with_pk_view, name="detail"),
    path('<slug>/update', post_api_update_survey_view, name="update"),
    path('<slug>/delete', post_api_delete_survey_view, name="delete"),
    path('create', post_api_create_survey_view, name="create"),
    path('list', post_ApiSurveyListView.as_view(), name="list"),
    path('<slug>/is_author', post_api_is_author_of_survey, name="is_author"),
]
