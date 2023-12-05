# Generated by Django 4.2.7 on 2023-12-05 17:19

import authentication.models.access_token
import authentication.models.action
import authentication.models.otp
import authentication.models.refresh_token
import authentication.models.user
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils.models
import utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-date_joined'],
            },
            managers=[
                ('objects', authentication.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('is_visible', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', related_query_name='child', to='authentication.action')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', utils.models.Manager()),
                ('roots', authentication.models.action.RootActionManager()),
            ],
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('email', 'email'), ('mobile', 'mobile')], max_length=10)),
                ('credential', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credentials', related_query_name='credential', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', utils.models.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('key', models.CharField(blank=True, default=None, max_length=20, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', utils.models.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='RefreshToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('token', models.CharField(db_index=True, default=authentication.models.refresh_token.default_refresh_token, max_length=40, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', utils.models.Manager()),
                ('alives', utils.models.DeletableAliveManager()),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=authentication.models.otp.default_otp_code, max_length=6, validators=[utils.validators.Code])),
                ('send_count', models.IntegerField(default=0)),
                ('tried_count', models.IntegerField(default=0)),
                ('last_send', models.DateTimeField(default=None, null=True)),
                ('last_tried', models.DateTimeField(default=None, null=True)),
                ('credential', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.credential')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', authentication.models.otp.OTPManager()),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', related_query_name='membership', to='authentication.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', related_query_name='membership', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', utils.models.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('granted', models.BooleanField(default=True)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', related_query_name='log', to='authentication.action')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', related_query_name='log', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', utils.models.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grants', related_query_name='grant', to='authentication.action')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grants', related_query_name='grant', to='authentication.group')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', utils.models.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('token', models.CharField(db_index=True, default=authentication.models.access_token.default_access_token, max_length=40, unique=True)),
                ('expire_at', models.DateTimeField(default=authentication.models.access_token.default_access_token_expire)),
                ('refresh', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='authentication.refreshtoken')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', authentication.models.access_token.AccessTokenManager()),
                ('alives', utils.models.DeletableAliveManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='actions',
            field=models.ManyToManyField(blank=True, related_name='users', related_query_name='user', to='authentication.action'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='users', related_query_name='user', through='authentication.Membership', to='authentication.group'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
