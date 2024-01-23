# Generated by Django 5.0 on 2023-12-28 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ecom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('digitalwatch', 'digitalwatch'), ('analogwatch', 'analogwatch')], default='digitalwatch', max_length=50)),
                ('image', models.ImageField(upload_to='images')),
                ('price', models.IntegerField()),
            ],
        ),
    ]