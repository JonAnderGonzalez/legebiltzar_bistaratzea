# Generated by Django 3.2.3 on 2021-06-01 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bis', '0002_auto_20210531_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='testua',
            name='entitateak_stopwords',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='testua',
            name='lemma',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='testua',
            name='tf_idf',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='testua',
            name='entitateak',
            field=models.TextField(default=''),
        ),
    ]
