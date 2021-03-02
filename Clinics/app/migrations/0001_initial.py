# Generated by Django 3.1.6 on 2021-03-02 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Methods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('therapy', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Clinicus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idrecord', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=60)),
                ('wightlrgfoto', models.IntegerField()),
                ('lenghtlrgfoto', models.IntegerField()),
                ('urlslrgefoto', models.URLField()),
                ('urlssmlfoto', models.URLField()),
                ('timeload', models.DateField(auto_now_add=True)),
                ('method', models.ManyToManyField(to='app.Methods')),
            ],
        ),
    ]
