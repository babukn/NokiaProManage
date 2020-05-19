from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

#from ...account.models import Account
from ..models import Survey
from ..api.serializers import SurveySerializer, SurveyUpdateSerializer, SurveyCreateSerializer,SurveySerializerThumnail

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/survey/<slug>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_detail_survey_view(request, slug):
	try:
		survey = Survey.objects.get(slug=slug)
	except Survey.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = SurveySerializer(survey)
		return Response(serializer.data)

#http://192.168.43.148:8000/api/survey/pk/13	pk based serch
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_full_image_with_pk_view(request,pk):
	try:
		survey = Survey.objects.get(pk=pk)
	except Survey.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		serializer = SurveySerializer(survey)
		return Response(serializer.data)
# Response: https://gist.github.com/mitchtabian/32507e93c530aa5949bc08d795ba66df
# Url: https://<your-domain>/api/survey/<slug>/update
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_survey_view(request, slug):

	try:
		survey = Survey.objects.get(slug=slug)
	except Survey.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if survey.author != user:
		return Response({'response':"You don't have permission to edit that."}) 
		
	if request.method == 'PUT':
		serializer = SurveyUpdateSerializer(survey, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS
			data['pk'] = survey.pk
			data['title'] = survey.title
			data['description'] = survey.description
			data['slug'] = survey.slug
			data['date_updated'] = survey.date_updated
			image_url = str(request.build_absolute_uri(survey.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			data['username'] = survey.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_is_author_of_survey(request, slug):
	try:
		survey = Survey.objects.get(slug=slug)
	except Survey.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if survey.author != user:
		data['response'] = "You don't have permission to edit that."
		return Response(data=data)
	data['response'] = "You have permission to edit that."
	return Response(data=data)


# Response: https://gist.github.com/mitchtabian/a97be3f8b71c75d588e23b414898ae5c
# Url: https://<your-domain>/api/survey/<slug>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE',])
@permission_classes((IsAuthenticated, ))
def api_delete_survey_view(request, slug):

	try:
		survey = Survey.objects.get(slug=slug)
	except Survey.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if survey.author != user:
		return Response({'response':"You don't have permission to delete that."}) 

	if request.method == 'DELETE':
		operation = survey.delete()
		data = {}
		if operation:
			data['response'] = DELETE_SUCCESS
		return Response(data=data)


# Response: https://gist.github.com/mitchtabian/78d7dcbeab4135c055ff6422238a31f9
# Url: https://<your-domain>/api/survey/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_survey_view(request):

	if request.method == 'POST':

		data = request.data
		data['author'] = request.user.pk
		serializer = SurveyCreateSerializer(data=data)

		data = {}
		if serializer.is_valid():
			survey = serializer.save()
			data['response'] = CREATE_SUCCESS
			data['pk'] = survey.pk
			data['title'] = survey.title
			data['description'] = survey.description
			data['slug'] = survey.slug
			data['date_updated'] = survey.date_updated
			image_url = str(request.build_absolute_uri(survey.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			data['username'] = survey.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: 
#		1) list: https://<your-domain>/api/survey/list
#		2) pagination: http://<your-domain>/api/survey/list?page=2
#		3) search: http://<your-domain>/api/survey/list?search=mitch
#		4) ordering: http://<your-domain>/api/survey/list?ordering=-date_updated
#		4) search + pagination + ordering: <your-domain>/api/survey/list?search=mitch&page=2&ordering=-date_updated
# Headers: Authorization: Token <token>
class ApiSurveyListView(ListAPIView):
	queryset = Survey.objects.all()
	serializer_class = SurveySerializerThumnail
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('title', 'description', 'author__username')