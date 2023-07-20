# Generated by Django 4.2.2 on 2023-06-12 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_is_verified_alter_customuser_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=150, null=True)),
                ('model', models.CharField(blank=True, max_length=150, null=True)),
                ('status', models.BooleanField(blank=True, default=False, help_text='0-show,1-Hidden')),
            ],
        ),
    ]
