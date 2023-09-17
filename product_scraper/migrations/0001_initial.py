# Generated by Django 3.2.16 on 2023-09-17 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=5000)),
                ('price', models.CharField(max_length=5000)),
                ('url', models.CharField(max_length=5000)),
                ('source', models.CharField(default='ebay', max_length=5000)),
            ],
        ),
    ]
