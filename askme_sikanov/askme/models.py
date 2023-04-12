from datetime import timezone
import datetime
from django.db.models import Count
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='../static/css/img/', default='photo.png')


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.name}'


class QuestionManager(models.Manager):
    def get_best(self):
        return self.annotate(num_likes=Count('likes')).filter(num_likes__gt=20)
    
    def get_new(self):
        return self.filter(create_date__gte=timezone.now() - datetime.timedelta(days=7))
    
    def by_tag(self, tag_name):
        return self.filter(tag__name=tag_name)


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
    