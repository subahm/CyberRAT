# Generated by Django 2.1.7 on 2019-07-15 22:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('CyberRATWeb', '0002_search_linkedin_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='uuid',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True),
        ),
    ]
