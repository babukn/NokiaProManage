from django.urls import path
from ..api.views import(
	api_detail_survey_view,
	api_update_survey_view,
	api_delete_survey_view,
	api_create_survey_view,
	api_is_author_of_survey,
	ApiSurveyListView,
	api_full_image_with_pk_view
)

app_name = 'sites.survey'

urlpatterns = [
	path('<slug>/', api_detail_survey_view, name="detail"),
	path('pk/<int:pk>/', api_full_image_with_pk_view, name="detail"),
	path('<slug>/update', api_update_survey_view, name="update"),
	path('<slug>/delete', api_delete_survey_view, name="delete"),
	path('create', api_create_survey_view, name="create"),
	path('list', ApiSurveyListView.as_view(), name="list"),
	path('<slug>/is_author', api_is_author_of_survey, name="is_author"),
]
