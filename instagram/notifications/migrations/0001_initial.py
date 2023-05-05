# Generated by Django 4.1.7 on 2023-05-04 01:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('follower', 'New follower'), ('like', 'New like'), ('comment', 'New comment')], max_length=155, verbose_name='category')),
                ('object_id', models.IntegerField(blank=True, null=True, verbose_name='object id')),
                ('object_slug', models.CharField(blank=True, max_length=200, null=True, verbose_name='object slug')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='slug')),
                ('is_read', models.BooleanField(default=False, verbose_name='is read')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]
