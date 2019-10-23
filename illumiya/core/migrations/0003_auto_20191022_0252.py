# Generated by Django 2.2.6 on 2019-10-22 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20191018_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=False, to='core.BlogTopic'),
        ),
    ]