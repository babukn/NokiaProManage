from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import Account
from ..models import Project, Task
from .serializers import ProjectSerializers, TaskSerializers, ProjectCreateSerializers, UserSerializer,TaskUpdateSerializer, TaskCreateSerializers

#http://192.168.43.148:8000/api/projectmanage/4/update
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def api_update_task_view(request,pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    print(task)

    if request.method == 'PUT':
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        data ={}
        if serializer.is_valid():
            serializer.save()
        return Response('done')

# http://192.168.43.148:8000/api/projectmanage/projectcreate
# {
# 	"name":"testpro3",
# 	"users":[3,4]
# }


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_project_view(request):
    if request.method == 'POST':
        data = request.data
        print(data)
        # print(user_account)
        # for user in data['users']:
        #     print(user)
        # data['users'] = 'kn'
        serializer = TaskCreateSerializers(data=data)

        data = {}
        if serializer.is_valid():
            task = serializer.save()
            data['response'] = 'created'
            data['name'] = task.name
            users = Account.objects.all()
            print(users)
            # data['users'] = project.users
            print(data)
            return Response(data)
        print(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#http://192.168.43.148:8000/api/projectmanage/projectcreate
# {
# 	"project":30,
# 	"name":"testproject",
# 	"assignee":[3,4],
# 	"progress":"10",
# 	"state":"to-do",
# 	"priority":"10_normal"
# }
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_task_view(request):
    if request.method == 'POST':
        data = request.data
        print(data)
        # print(user_account)
        for user in data['users']:
            print(user)
        # data['users'] = 'kn'
        serializer = T(data=data)

        data = {}
        if serializer.is_valid():
            project = serializer.save()
            data['response'] = 'created'
            data['name'] = project.name
            users = Account.objects.all()
            print(users)
            # data['users'] = project.users
            print(data)
            return Response(data)
        print(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# http://192.168.43.148:8000/api/projectmanage/projectlist
# http://192.168.43.148:8000/api/projectmanage/projectlist?search=itn
class ProjectView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('users__username', 'id', 'name')


# http://192.168.43.148:8000/api/projectmanage/tasklist?search=itn
# http://192.168.43.148:8000/api/projectmanage/tasklist
class TaskView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('assignee__username', 'assignee__email','id', 'project__name', 'name')

## http://192.168.43.148:8000/api/projectmanage/userlist get userlist with id
class ListUser(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('id', 'username')
