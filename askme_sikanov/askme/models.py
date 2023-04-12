from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)
    avatar_url = models.URLField(max_length=255)


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    create_date = models.DateField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)


class Answer(models.Model):
    text = models.TextField()
    correct = models.BooleanField()
    create_date = models.DateField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Like(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('content_type', 'object_id', 'profile')
    