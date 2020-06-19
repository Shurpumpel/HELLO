from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Sum

# Create your models here.

class Persons(models.Model):
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)
    town = models.CharField(max_length=30)

class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def books(self):
        return self.get_queryset().all()

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )
    objects = LikeDislikeManager()
    vote = models.SmallIntegerField(choices=VOTES, default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    year = models.SmallIntegerField()
    publishing = models.CharField(max_length=20)
    possibility = models.CharField(max_length=50)
    wish = models.CharField(max_length=100)
    image = models.ImageField(upload_to="C:/django/hello/media/user_book")
    personid = models.ForeignKey(Persons, on_delete=models.CASCADE)
    votes = GenericRelation(LikeDislike, related_query_name='books')