# Generated by Django 2.2 on 2019-05-16 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(blank=True, max_length=140, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=140, verbose_name='Last name')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, verbose_name='Mobile phone')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False, verbose_name='Account ID')),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True, verbose_name='Total balance')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Start time')),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_accounts', to=settings.AUTH_USER_MODEL, verbose_name='UserProfile')),
            ],
        ),
    ]
