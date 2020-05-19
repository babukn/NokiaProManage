from django.urls import path
from ..api.views import (
    ProjectView,
    TaskView,
    api_create_project_view,
    ListUser,
    api_update_task_view,
    api_create_task_view,
)

app_name = 'porjectmanage'

urlpatterns = [
    # preInstalation
    path('projectlist', ProjectView.as_view(), name="projectlist"),
    path('tasklist', TaskView.as_view(), name="tasklist"),
    path('userlist', ListUser.as_view(), name="userlist"),
    path('projectcreate', api_create_project_view, name="projectcreate"),
    path('taskcreate', api_create_task_view, name="taskcreate"),
    path('<int:pk>/update',api_update_task_view,name="updateTask")

]
