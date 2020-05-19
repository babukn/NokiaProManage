from rest_framework import serializers, viewsets

from account.models import Account
from ..models import Project, Task
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:

        model = Account
        fields = ['id', 'email']


class Projectseralizerfindpro(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name']


class ProjectSerializers(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'users']

    # def get_username_from_users(self, project):
    #     username = project.objects.get(pk=1)
    #     print(username)
    #     return username


class ProjectCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'users']

        def save(self):
            try:
                name = self.validated_data['name']
                users = self.validated_data['users']

                project = Project(name=name,
                                  users=users)
                project.save()
                return project
            except KeyError:
                raise serializers.ValidationError({"responce": "you must have project nam and assosiated users"})


class TaskCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['project', 'name', 'assignee', 'progress', 'state', 'priority']

        def save(self):
            try:
                project = self.validated_data['project']
                name = self.validated_data['name']
                assignee = self.validate_data['assignee']
                progress = self.valiate_data['progress']
                state = self.validate_data['state']
                priority = self.validate_data['priority']

                task = Task(project=project, name=name, assignee=assignee, progress=progress, state=state,
                            priority=priority)
                task.save()
                return task
            except KeyError:
                raise serializers.ValidationError({"responce": "you must have task name and assosiated users"})


class TaskSerializers(serializers.ModelSerializer):
    assignee = UserSerializer(many=True, read_only=True)
    project = Projectseralizerfindpro(many=False, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'project', 'name', 'assignee', 'progress', 'state', 'priority']


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['project', 'name', 'assignee', 'progress', 'state', 'priority']
