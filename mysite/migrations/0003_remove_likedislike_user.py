# Generated by Django 3.0.7 on 2020-06-18 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_book_likedislike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likedislike',
            name='user',
        ),
    ]