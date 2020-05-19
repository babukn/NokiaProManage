from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

#from ...account.models import Account
from ..models import Predismantle, Postdismantle
from ..api.serializers import PredismantleSerializer, PredismantleUpdateSerializer, PredismantleCreateSerializer,PostdismantleSerializer,PostdismantleUpdateSerializer,PostdismantleCreateSerializer,PostdismantleSerializerThumnail,PredismantleSerializerThumnail

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

#preinstalation
# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/survey/<slug>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def pre_api_detail_survey_view(request, slug):

	try:
		pre_dismantle = Predismantle.objects.get(slug=slug)
	except Predismantle.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = PredismantleSerializer(pre_dismantle)
		return Response(serializer.data)

#http://192.168.43.148:8000/api/survey/pk/13	pk based serch
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def pre_api_full_image_with_pk_view(request,pk):
	try:
		pre_dismantle = Predismantle.objects.get(pk=pk)
	except Predismantle.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		serializer = PredismantleSerializer(pre_dismantle)
		return Response(serializer.data)
# Response: https://gist.github.com/mitchtabian/32507e93c530aa5949bc08d795ba66df
# Url: https://<your-domain>/api/survey/<slug>/update
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def pre_api_update_survey_view(request, slug):

	try:
		pre_dismantle = Predismantle.objects.get(slug=slug)
	except Predismantle.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if pre_dismantle.author != user:
		return Response({'response':"You don't have permission to edit that."}) 
		
	if request.method == 'PUT':
		serializer = PredismantleUpdateSerializer(pre_dismantle, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS
			data['pk'] = pre_dismantle.pk
			data['title'] = pre_dismantle.title
			data['description'] = pre_dismantle.description
			data['slug'] = pre_dismantle.slug
			data['date_updated'] = pre_dismantle.date_updated
			image_url = str(request.build_absolute_uri(pre_dismantle.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			data['username'] = pre_dismantle.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def pre_api_is_author_of_survey(request, slug):
	try:
		pre_dismantle = Predismantle.objects.get(slug=slug)
	except Predismantle.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if pre_dismantle.author != user:
		data['response'] = "You don't have permission to edit that."
		return Response(data=data)
	data['response'] = "You have permission to edit that."
	return Response(data=data)


# Response: https://gist.github.com/mitchtabian/a97be3f8b71c75d588e23b414898ae5c
# Url: https://<your-domain>/api/survey/<slug>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE',])
@permission_classes((IsAuthenticated, ))
def pre_api_delete_survey_view(request, slug):

	try:
		pre_dismantle = Predismantle.objects.get(slug=slug)
	except Predismantle.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if pre_dismantle.author != user:
		return Response({'response':"You don't have permission to delete that."}) 

	if request.method == 'DELETE':
		operation = pre_dismantle.delete()
		data = {}
		if operation:
			data['response'] = DELETE_SUCCESS
		return Response(data=data)


# Response: https://gist.github.com/mitchtabian/78d7dcbeab4135c055ff6422238a31f9
# Url: https://<your-domain>/api/survey/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def pre_api_create_survey_view(request):

	if request.method == 'POST':

		data = request.data
		data['author'] = request.user.pk
		serializer = PredismantleCreateSerializer(data=data)

		data = {}
		if serializer.is_valid():
			pre_dismantle = serializer.save()
			data['response'] = CREATE_SUCCESS
			data['pk'] = pre_dismantle.pk
			data['title'] = pre_dismantle.title
			data['description'] = pre_dismantle.description
			data['slug'] = pre_dismantle.slug
			data['date_updated'] = pre_dismantle.date_updated
			image_url = str(request.build_absolute_uri(pre_dismantle.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			data['username'] = pre_dismantle.author.username
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
class pre_ApidismantleListView(ListAPIView):
	queryset = Predismantle.objects.all()
	serializer_class = PredismantleSerializerThumnail
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('title', 'description', 'author__username')


#post instalation

# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/survey/<slug>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def post_api_detail_survey_view(request, slug):
	try:
		post_dismantle = Postdismantle.objects.get(slug=slug)
	except Postdismantle.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = PostdismantleSerializer(post_dismantle)
		return Response(serializer.data)


#http://192.168.43.148:8000/api/survey/pk/13	pk based serch
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def post_api_full_image_with_pk_view(request,pk):
	try:
		post_dismantle = Postdismantle.objects.get(pk=pk)
	except Postdismantle.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		serializer = PostdismantleSerializer(post_dismantle)
		return Response(serializer.data)

# Response: https://gist.github.com/mitchtabian/32507e93c530aa5949bc08d795ba66df
# Url: https://<your-domain>/api/survey/<slug>/update
# Headers: Authorization: Token <token>
@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def post_api_update_survey_view(request, slug):
	try:
		post_dismantle = Postdismantle.objects.get(slug=slug)
	except Postdismantle.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if post_dismantle.author != user:
		return Response({'response': "You don't have permission to edit that."})

	if request.method == 'PUT':
		serializer = PostdismantleUpdateSerializer(post_dismantle, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS
			data['pk'] = post_dismantle.pk
			data['title'] = post_dismantle.title
			data['description'] = post_dismantle.description
			data['slug'] = post_dismantle.slug
			data['date_updated'] = post_dismantle.date_updated
			image_url = str(request.build_absolute_uri(post_dismantle.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			data['username'] = post_dismantle.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def post_api_is_author_of_survey(request, slug):
	try:
		post_dismantle = Postdismantle.objects.get(slug=slug)
	except Postdismantle.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if post_dismantle.author != user:
		data['response'] = "You don't have permission to edit that."
		return Response(data=data)
	data['response'] = "You have permission to edit that."
	return Response(data=data)


# Response: https://gist.github.com/mitchtabian/a97be3f8b71c75d588e23b414898ae5c
# Url: https://<your-domain>/api/survey/<slug>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def post_api_delete_survey_view(request, slug):
	try:
		post_dismantle = Postdismantle.objects.get(slug=slug)
	except Postdismantle.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if post_dismantle.author != user:
		return Response({'response': "You don't have permission to delete that."})

	if request.method == 'DELETE':
		operation = post_dismantle.delete()
		data = {}
		if operation:
			data['response'] = DELETE_SUCCESS
		return Response(data=data)


# Response: https://gist.github.com/mitchtabian/78d7dcbeab4135c055ff6422238a31f9
# Url: https://<your-domain>/api/survey/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def post_api_create_survey_view(request):
	if request.method == 'POST':

		data = request.data
		data['author'] = request.user.pk
		serializer = PostdismantleCreateSerializer(data=data)

		data = {}
		if serializer.is_valid():
			post_dismantle = serializer.save()
			data['response'] = CREATE_SUCCESS
			data['pk'] = post_dismantle.pk
			data['title'] = post_dismantle.title
			data['description'] = post_dismantle.description
			data['slug'] = post_dismantle.slug
			data['date_updated'] = post_dismantle.date_updated
			image_url = str(request.build_absolute_uri(post_dismantle.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			data['username'] = post_dismantle.author.username
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
class post_ApidismantleListView(ListAPIView):
	queryset = Postdismantle.objects.all()
	serializer_class = PostdismantleSerializerThumnail
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('title', 'description', 'author__username')