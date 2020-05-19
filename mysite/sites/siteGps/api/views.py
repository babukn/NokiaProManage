from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

# from ...account.models import Account
from ..models import SiteGps
from .serializers import SiteGpsSerializer, SiteGpsCreateSerializer
SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

#http://127.0.0.1:8000/api/sitegps/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_site_gps(request):
    request.POST._mutable = True
    print(request.user.pk)
    if request.method == 'POST':
        data = request.data
        data['author'] = request.user.pk
        serializer = SiteGpsCreateSerializer(data=data)

        data = {}
        if serializer.is_valid():
            site_gps = serializer.save()
            data['response'] = CREATE_SUCCESS
            data['pk'] = site_gps.pk
            data['site_id'] = site_gps.site_id
            data['long_lang'] = site_gps.long_lang
            data['date_updated'] = site_gps.date_updated
            data['username'] = site_gps.author.username
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#http://127.0.0.1:8000/api/sitegps
# #for listing all sites with 10 paged for changing page go settings
class api_detail_sitegps_view(ListAPIView):
    queryset = SiteGps.objects.get_queryset().order_by('id')
    serializer_class = SiteGpsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('site_id', 'long_lang', 'date_updated','author__username')
