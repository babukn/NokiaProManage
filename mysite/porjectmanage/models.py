from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='usernames')

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUSES = (
        ('to-do', _('To Do')),
        ('in_progress', _('In Progress')),
        ('blocked', _('Blocked')),
        ('done', _('Done')),
        ('dismissed', _('Dismissed'))
    )
    PRIORITIES = (
        ('Low', _('Low')),
        ('Normal', _('Normal')),
        ('High', _('High')),
        ('Critical', _('Critical')),
        ('blocker', _('Blocker'))
    )
    project = models.ForeignKey(Project, related_name='project_tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    # assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='assignees')
    progress = models.CharField(max_length=302, null=True)
    state = models.CharField(_("state"), max_length=20, choices=STATUSES, default='to-do')
    priority = models.CharField(_("priority"), max_length=20, choices=PRIORITIES, default='10_normal')

    def __str__(self):
        return self.name


##Get the the users participating in a specific project:
# p = Project.objects.get(name='myproject')
# users = p.users.all()
##Get a project's tasks:
# users = p.project_tasks.all()  # Because of `related_name` in Task.project
##Get All the tasks a user has, of all the projects:
# u = User.objects.get(username='someuser')
# u.tasks.all()  # Because of `related_name` in Task.assignee
