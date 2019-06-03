# Generated by Django 2.1.7 on 2019-03-23 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwtimple', '0002_auto_20190323_2332'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.IntegerField(default=0)),
                ('updated_by', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'module_actions',
            },
        ),
    ]