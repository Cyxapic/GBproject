# Generated by Django 2.0.7 on 2018-07-16 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=30, verbose_name='Имя URL')),
                ('title', models.CharField(max_length=45, verbose_name='Отображаемое имя')),
                ('posnum', models.PositiveSmallIntegerField(verbose_name='Позиция вывод')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
                'ordering': ('posnum',),
            },
        ),
    ]