# Generated by Django 4.0.2 on 2022-04-26 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieHome', '0002_delete_survey'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('que_id', models.AutoField(primary_key=True, serialize=False)),
                ('que', models.CharField(max_length=256)),
                ('original_answer', models.TextField()),
            ],
        ),
    ]
