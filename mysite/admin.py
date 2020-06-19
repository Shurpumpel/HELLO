from django.contrib import admin

# Register your models here.

from .models import Persons, Book, LikeDislike

admin.site.register(Book)
admin.site.register(Persons)
admin.site.register(LikeDislike)