# Generated by Django 2.2 on 2021-05-28 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0003_post_user_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comment_likes',
            field=models.ManyToManyField(related_name='like_comment', to='login_app.User'),
        ),
    ]
