# Generated by Django 4.1.3 on 2022-11-25 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_blog_blogsection'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='audience',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='topic',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]