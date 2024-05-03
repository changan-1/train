# Generated by Django 3.2.13 on 2024-04-26 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selectlocal', '0003_delete_wantgo'),
    ]

    operations = [
        migrations.CreateModel(
            name='wantGo',
            fields=[
                ('cityId', models.BigAutoField(primary_key=True, serialize=False)),
                ('imgUrl', models.CharField(blank=True, max_length=60, null=True)),
                ('cityName', models.CharField(blank=True, max_length=60, null=True)),
                ('selectId', models.IntegerField(blank=True, max_length=6, null=True)),
            ],
            options={
                'db_table': 'want_go',
                'managed': False,
            },
        ),
    ]