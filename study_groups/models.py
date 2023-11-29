# study_groups/models.py

from django.db import models
from django.contrib.auth.models import User


class StudyGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='study_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupPermission(models.Model):
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_post = models.BooleanField(default=True)
    can_comment = models.BooleanField(default=True)
    can_invite = models.BooleanField(default=False)


class Message(models.Model):
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

