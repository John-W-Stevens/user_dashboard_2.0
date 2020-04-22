# Generated by Django 2.2 on 2020-04-22 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('level', models.IntegerField(default=1)),
                ('description', models.TextField(null=True)),
                ('password', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile_photo', models.ImageField(blank=True, upload_to='profile_images')),
                ('default_photo', models.ImageField(default='default.jpg', upload_to='profile_images')),
                ('city', models.CharField(max_length=45, null=True)),
                ('state', models.CharField(max_length=45, null=True)),
                ('country', models.CharField(max_length=45, null=True)),
            ],
        ),
    ]
